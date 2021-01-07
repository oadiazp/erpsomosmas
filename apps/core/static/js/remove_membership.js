$(function() {
   $('.btn-warning').click(function () {
       const response = confirm('¿Seguro?');

       if (response) {
           window.location.href = '/accounts/remove_membership'
       }
   });
});