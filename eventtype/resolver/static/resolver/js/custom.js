
window.addEventListener('message', function(event) {
    if ( "pennytoken-protocol-version" in event.data){
        console.log('page javascript got message');
        $(".plugin_not_present").hide();
        $(".plugin_present").show();
    }
});


// Sets active link in Bootstrap menu
// Add this code in a central place used\shared by all pages
// like your _Layout.cshtml in ASP.NET MVC for example
$('a[href="' + this.location.pathname + '"]').parents('li,ul').addClass('active');