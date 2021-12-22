$(document).ready(function(){
    $("#about-btn").click(function(event){
        alert ("You clicked on the button using Jquery!");
    });
    
    $("p").hover(function(){
        $(this).css('color', 'red');
    },
    function(){
        $(this).css('color', 'black');
    });

    $("#about-btn").click(function(event){
        msgstr = $("#msg").html()
        msgstr = msgstr + "ooo"
        $("#msg").html(msgstr)
    });
});