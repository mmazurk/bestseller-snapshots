  
  
  // Add a click event listener to all the "Go to List!" links on the page
  $('#container-div').on('click', "a", function(event) {
    // Prevent the default link behavior
    
    if ($(this).text() === "Go to List!") {

        event.preventDefault();

        const listNameEncoded = $(this).attr('id');
        console.log(listNameEncoded)
    
        const dateField = $('#' + listNameEncoded + '_date');
        console.log(dateField.val())
    
        const linkUrl = $(this).attr('href') + '&date=' + dateField.val();
        console.log(linkUrl)
    
        window.location.href = linkUrl;
    
    }

});   