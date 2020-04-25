paypal.Buttons({
    createSubscription: function (data, actions) {
        return actions.subscription.create({
            'plan_id': $('#plan_id').val()
        });
    },
    onApprove: function (data, actions) {
        actions.order.get().then(function (details) {
            console.log(details);
            window.location.href = '/accounts/set_paypal_email?email=' + details.payer.email_address + '&order_id=' + details.id;
        });
    }
}).render('#button_paypal');