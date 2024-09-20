// PDF.js related variables
let pdfDoc = null;

// Load the PDF
const pdfUrl = 'JaeHongLee_Studybook.pdf'; // Replace with your PDF file path

pdfjsLib.getDocument(pdfUrl).promise.then(function(pdf) {
  pdfDoc = pdf;

  // Render the first 3 pages
  renderPage(1, 'pdf-canvas1');
  renderPage(2, 'pdf-canvas2');
  renderPage(3, 'pdf-canvas3');
  
  // Initialize the turn.js flipbook
  $('.flipbook').turn({
    width: 800,
    height: 500,
    autoCenter: true
  });
});

function renderPage(pageNum, canvasId) {
  pdfDoc.getPage(pageNum).then(function(page) {
    const canvas = document.getElementById(canvasId);
    const ctx = canvas.getContext('2d');
    const viewport = page.getViewport({ scale: 1.5 });

    canvas.height = viewport.height;
    canvas.width = viewport.width;

    const renderContext = {
      canvasContext: ctx,
      viewport: viewport
    };

    page.render(renderContext);
  });
}