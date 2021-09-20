$("div[id^='saleModal']").each(function(){
  
  var currentModal = $(this);
  
  //click next
  currentModal.find('.btn-next').click(function(){
    currentModal.modal('hide');
    currentModal.closest("div[id^='saleModal']").nextAll("div[id^='saleModal']").first().modal('show'); 
  });
  
//   //click prev
//   currentModal.find('.btn-prev').click(function(){
//     currentModal.modal('hide');
//     currentModal.closest("div[id^='saleModal']").prevAll("div[id^='saleModal']").first().modal('show'); 
//   });

});

$("div[id^='intakeModal']").each(function(){
  
  var currentModal = $(this);
  
  //click next
  currentModal.find('.btn-next').click(function(){
    currentModal.modal('hide');
    currentModal.closest("div[id^='intakeModal']").nextAll("div[id^='intakeModal']").first().modal('show'); 
  });
  
//   //click prev
//   currentModal.find('.btn-prev').click(function(){
//     currentModal.modal('hide');
//     currentModal.closest("div[id^='saleModal']").prevAll("div[id^='saleModal']").first().modal('show'); 
//   });

});


$("div[id^='sampleModal']").each(function(){
  
  var currentModal = $(this);
  
  //click next
  currentModal.find('.btn-next').click(function(){
    currentModal.modal('hide');
    currentModal.closest("div[id^='sampleModal']").nextAll("div[id^='sampleModal']").first().modal('show'); 
  });
  
//   //click prev
//   currentModal.find('.btn-prev').click(function(){
//     currentModal.modal('hide');
//     currentModal.closest("div[id^='saleModal']").prevAll("div[id^='saleModal']").first().modal('show'); 
//   });

});
