#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_YEAR_DURATION	10	// 기간

// 구조체 선언
typedef struct {
	char	name[20];		// 이름
	char	sex;			// 성별 M or F
	int		freq[MAX_YEAR_DURATION]; // 연도별 빈도
} tName; //mnset

typedef struct {
	int		len;		// 배열에 저장된 이름의 수
	int		capacity;	// 배열의 용량 (배열에 저장 가능한 이름의 수)
	tName	*data;		// 이름 배열의 포인터
} tNames;

////////////////////////////////////////////////////////////////////////////////
// 함수 원형 선언

// 입력 파일을 읽어 이름 정보(연도, 이름, 성별, 빈도)를 이름 구조체에 저장
// 이미 구조체에 존재하는(저장된) 이름은 해당 연도의 빈도만 저장
// 새로 등장한 이름은 구조체에 추가
// 주의사항: 동일 이름이 남/여 각각 사용될 수 있으므로, 이름과 성별을 구별해야 함
// 주의사항: 정렬 리스트(ordered list)를 유지해야 함 (qsort 함수 사용하지 않음)
// 이미 등장한 이름인지 검사하기 위해 bsearch 함수를 사용 c언어의 bsearch 함수
// 새로운 이름을 저장할 메모리 공간을 확보하기 위해 memmove 함수를 이용하여 메모리에 저장된 내용을 복사
// names->capacity는 1000으로부터 시작하여 1000씩 증가 (1000, 2000, 3000, ...)
// start_year : 시작 연도 (2009)
void load_names( FILE *fp, int start_year, tNames *names);

// 구조체 배열을 화면에 출력
void print_names( tNames *names, int num_year);

// bsearch를 위한 비교 함수
// 정렬 기준 : 이름(1순위), 성별(2순위)
int compare( const void *n1, const void *n2);

// 이진탐색 함수
// return value: key가 발견되는 경우, 배열의 인덱스
//				key가 발견되지 않는 경우, key가 삽입되어야 할 배열의 인덱스
int binary_search( const void *key, const void *base, size_t nmemb, size_t size, int (*compare)(const void *, const void *));

////////////////////////////////////////////////////////////////////////////////
// 함수 정의

// 이름 구조체 초기화
// len를 0으로, capacity를 1로 초기화
// return : 구조체 포인터
tNames *create_names(void)
{
	tNames *pnames = (tNames *)malloc( sizeof(tNames));
	
	pnames->len = 0;
	pnames->capacity = 1000;
	pnames->data = (tName *)malloc(pnames->capacity * sizeof(tName));

	return pnames;
}

// 이름 구조체에 할당된 메모리를 해제
void destroy_names(tNames *pnames)
{
	free(pnames->data);
	pnames->len = 0;
	pnames->capacity = 0;

	free(pnames);
}
	
////////////////////////////////////////////////////////////////////////////////
int main(int argc, char **argv)
{
	tNames *names;
	FILE *fp;
	
	if (argc != 2)
	{
		fprintf( stderr, "Usage: %s FILE\n\n", argv[0]);
		return 1;
	}

	// 이름 구조체 초기화
	names = create_names();
	
	fp = fopen( argv[1], "r");
	if (!fp)
	{
		fprintf( stderr, "cannot open file : %s\n", argv[1]);
		return 1;
	}

	fprintf( stderr, "Processing [%s]..\n", argv[1]);
		
	// 연도별 입력 파일(이름 정보)을 구조체에 저장
	load_names( fp, 2009, names);
	
	fclose( fp);
	
	// 이름 구조체를 화면에 출력
	print_names( names, MAX_YEAR_DURATION);

	// 이름 구조체 해제
	destroy_names( names);
	
	return 0;
}


void load_names( FILE *fp, int start_year, tNames *names){
	const int max = 255;
	char line[max], name[20], gender;
	int year, freq_value, insert_key;

	tName *find;
	tName *member = (tName *)malloc(sizeof(tName));

	while (fgets(line, sizeof(line), fp) != NULL){

		sscanf(line, "%d %s %c %d", &year, name, &gender, &freq_value);
		
		strcpy(member->name, name);
		member->sex = gender;

		if((find = bsearch(member, names->data, names->len, sizeof(tName), compare)) != NULL) 
		{
			find->freq[year-start_year] = freq_value;
		}else{
			insert_key = binary_search(member, names->data, names->len, sizeof(tName), compare);
			if(names->capacity == names->len){
				names->capacity += 1000;
				names->data = (tName *)realloc(names->data, names->capacity * sizeof(tName));
			}
			memmove(&(names->data[insert_key+1]), &(names->data[insert_key]), sizeof(tName) * (names->len - insert_key));
			memset(names->data[insert_key].freq, 0, MAX_YEAR_DURATION * sizeof(int));
			strcpy(names->data[insert_key].name, name);
			names->data[insert_key].sex = gender;
			names->data[insert_key].freq[year-start_year] = freq_value;
			names->len++;
		}
	}
	free(member);
}

// 이진탐색 함수
// return value: key가 발견되는 경우, 배열의 인덱스
//				key가 발견되지 않는 경우, key가 삽입되어야 할 배열의 인덱스
int binary_search( const void *key, const void *base, size_t nmemb, size_t size, int (*compare)(const void *, const void *)){
	tName *key_ptr = (tName *)key;
	tName *base_ptr = (tName *)base;

	int low, mid, high;
	tName *ptr;

	low = 0;
	high = nmemb - 1;

	while(low <= high){
		mid = (high + low) / 2;
		ptr = &(base_ptr[mid]);
		if(compare(ptr, key) == 0){
			return mid;
		} else if(compare(ptr, key) < 0 ){
			low = mid + 1;
		}else{
			high = mid - 1;	
		}
		if(low > high){
			return low;
		}
	}
	return 0;
}

void print_names( tNames *names, int num_year){
	tName *ptr;
	ptr = &(names->data[0]);
	for(int i = 0; i < names->len; i++){
		ptr = &(names->data[i]);
		printf( "%s\t%c", ptr->name, ptr->sex);
		for (int j = 0; j < num_year; j++){
			printf("\t%d", ptr->freq[j]);
		}
		printf("\n");
	}
}

int compare( const void *n1, const void *n2){
	tName *ptr1 = (tName *)n1;
	tName *ptr2 = (tName *)n2;

	if(strcmp(ptr1->name, ptr2->name) == 0){
		if(ptr1->sex == ptr2->sex){
			return 0;
		}
		else if(ptr1->sex == 'F'){
			return -1;
		}else{
			return 1;
		}
	}else if(strcmp(ptr1->name, ptr2->name) < 0){
		return -1;
	}else{
		return 1;
	}
}





























