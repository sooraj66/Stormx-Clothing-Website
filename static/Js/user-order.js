document.addEventListener('DOMContentLoaded', function () {
            const paymentMethodRadios = document.querySelectorAll('input[name="paymentMethod"]');
            const paymentOptions = {
                creditCard: document.getElementById('creditCard'),
                upi: document.getElementById('upi'),
                cashOnDelivery: document.getElementById('cashOnDelivery')
            };

            paymentMethodRadios.forEach(radio => {
                radio.addEventListener('change', function () {
                    for (const option in paymentOptions) {
                        paymentOptions[option].classList.remove('active');
                    }
                    const selectedOption = this.value;
                    if (paymentOptions[selectedOption]) {
                        paymentOptions[selectedOption].classList.add('active');
                    }
                });
            });
        });
