(function() {
  var stripe = Stripe('pk_test_RRtSzNdsTvSvgnN6uKGgssa700eJ348Znd');
  var competitions = document.getElementById('competitions').textContent;

  var cotisation = document.getElementById('cotisation').textContent;
  if (cotisation.includes('fille -11')) {
        sku = 'sku_H0o152HDnoijMK';
   } else if (cotisation.includes('enfant -11')){
        sku = 'sku_H0o4G3770euUBt';
   } else if (cotisation.includes('enfant +11')){
        sku = 'sku_H0o47Mg9NfDr6j';
   }else if (cotisation.includes('adulte competition')){
        sku = 'sku_H0hr9Uch0bwY8c';
   }else if (cotisation.includes('adulte loisir')){
        sku = 'sku_H0hsstf1idJ6vv';
   }

   var skus = [{sku: sku, quantity: 1}]
   if (competitions.includes('fscf')) {
        let insertsku2 = {sku: 'sku_H0o5uXOn12WmKh', quantity: 1};
        skus.push(insertsku2);
   }
   if (competitions.includes('indivs')) {
        let insertsku3 = {sku: 'sku_H0o5WmLc3UcAxJ', quantity: 1};
        skus.push(insertsku3);
   }

  var checkoutButton = document.getElementById('mon-bouton');
  checkoutButton.addEventListener('click', function () {
    // When the customer clicks on the button, redirect
    // them to Checkout.
    stripe.redirectToCheckout({
      items: skus,

      // Do not rely on the redirect to the successUrl for fulfilling
      // purchases, customers may not always reach the success_url after
      // a successful payment.
      // Instead use one of the strategies described in
      // https://stripe.com/docs/payments/checkout/fulfillment
      successUrl: 'http://127.0.0.1:8000/reuillytt/success/',
      cancelUrl: 'https://your-website.com/canceled',
    })
    .then(function (result) {
      if (result.error) {
        // If `redirectToCheckout` fails due to a browser or network
        // error, display the localized error message to your customer.
        var displayError = document.getElementById('error-message');
        displayError.textContent = result.error.message;
      }
    });
  });
})();