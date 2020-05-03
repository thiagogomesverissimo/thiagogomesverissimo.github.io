/* Minhas customizações */
$(document).ready(function(){
  var toc = document.getElementById('toc');
  toc.innerHTML = '<ul>';

  $('article .page__inner-wrap h2, article .page__inner-wrap h3').each(function() {

    var id = $(this).attr('id');
    if ($(this).prop("tagName") === 'H2') {
      toc.innerHTML += `<li><a href="#${id}">` + $(this).text() + '</a></li>';
    } else {
      toc.innerHTML += `<ul><li><a href="#${id}">` + $(this).text() + '</a></li></ul>';
    }


  });

  toc.innerHTML += '</ul>';

});
