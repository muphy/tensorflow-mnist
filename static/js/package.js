$(window).ready(function() {

  $('#request').click(function() {
    if(!$('#pop_id').val() || !$('#cover_code').val()) {
      alert("입력값을 확인하세요");
    }
    var params = {
       pop_id : $('#pop_id').val(),
       cover_code : $('#cover_code').val()
    };
    $.getJSON( "/api/packages/price", params, function( data ) {
      console.log(data);
//      alert(data.results.price);
      if(data.results.price == "0") {
         alert("cover_code 값에 매칭되는 cover_code 가 없습니다");
      }
      $('#result').text(data.results.price);
    });
  });


});