import numpy as np
from collections import defaultdict

class EWMAPredictor:
    def __init__(self, alpha=0.7):
        self.alpha = alpha
        self.current_estimate = None
        self.errors = []
    
    def update(self, actual_value):
        if self.current_estimate is None:
            self.current_estimate = actual_value
            return actual_value
        
        # Save current prediction
        prediction = self.current_estimate
        
        # Calculate prediction error and save
        error = abs(prediction - actual_value)
        self.errors.append(error)
        
        # Update EWMA
        self.current_estimate = self.alpha * actual_value + (1 - self.alpha) * self.current_estimate
        
        return prediction
    
    def get_average_error(self):
        if not self.errors:
            return 0
        return np.mean(self.errors)

def parse_server_output(filename):
    operations = defaultdict(list)
    
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('T0 R'):
                parts = line.strip().split(',')
                # T0 R1:2713582.267675,IMG_HORIZEDGES,1,0,0,2713582.267750,2713582.267818,2713582.293519
                # T<thread_id> R<request_id>:<send timestamp>,<operation>,<overwrite>,<client IMG ID>,<Server IMG ID>,<recv timestamp>,<start timestamp>,<end timestamp>
                if len(parts) >= 8 and 'IMG_RETRIEVE' not in parts[1]:
                    op_name = parts[1] # operation name
                    send_time = float(parts[6])  # send timestamp
                    complete_time = float(parts[7])  # complete timestamp
                    duration_microseconds = (complete_time - send_time) * 1_000_000
                    operations[op_name].append(duration_microseconds)
    
    return operations

def main():
    # Data parsing
    operations = parse_server_output('Eval_b_images_all.txt')  # or whichever file you want to analyze
    
    # Create EWMA predictors for each operation type
    predictors = {op_type: EWMAPredictor() for op_type in operations.keys()}
    
    # Perform predictions for each operation type
    for op_type, durations in operations.items():
        print(f"\nAnalyzing {op_type}:")
        predictor = predictors[op_type]
        
        for duration in durations:
            prediction = predictor.update(duration)
        
        avg_error = predictor.get_average_error()
        print(f"Average prediction error: {avg_error/1000:.2f}ms")
        print(f"Number of samples: {len(durations)}")
        print(f"Final EWMA estimate: {predictor.current_estimate/1000:.2f}ms")
        
        # Relative size of average error (error/average duration)
        avg_duration = np.mean(durations)
        relative_error = (avg_error / avg_duration) * 100
        print(f"Relative prediction error: {relative_error:.1f}%")

if __name__ == "__main__":
    main()