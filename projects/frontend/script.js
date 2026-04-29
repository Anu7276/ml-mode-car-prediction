document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    const modelSelect = document.getElementById('Car_Name');
    const carImage = document.getElementById('car-image');
    const carPlaceholder = document.getElementById('car-placeholder');
    const predictBtn = document.getElementById('predict-btn');
    
    const states = {
        default: document.getElementById('default-state'),
        success: document.getElementById('success-state')
    };

    const results = {
        price: document.getElementById('predicted-price'),
        range: document.getElementById('price-range')
    };

    // --- Car Image Mapping ---
    const carImages = {
        'Nexon': 'https://images.unsplash.com/photo-1623910384784-0678d91c107e?q=80&w=800',
        'Harrier': 'https://images.unsplash.com/photo-1632245889027-3a1e2f896984?q=80&w=800',
        'Safari': 'https://images.unsplash.com/photo-1632245889417-768565b991b1?q=80&w=800',
        'Punch': 'https://images.unsplash.com/photo-1625037553530-589632924976?q=80&w=800',
        'Altroz': 'https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?q=80&w=800',
        'Tiago': 'https://images.unsplash.com/photo-1631525048256-42d87e07669d?q=80&w=800'
    };

    modelSelect.addEventListener('change', (e) => {
        const val = e.target.value;
        if (carImages[val]) {
            carImage.src = carImages[val];
            carImage.classList.remove('hidden');
            carPlaceholder.classList.add('hidden');
        }
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        predictBtn.disabled = true;
        predictBtn.textContent = 'Calculating...';

        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        
        // Auto-calculate Car_Age
        const currentYear = new Date().getFullYear();
        data.Car_Age = currentYear - parseInt(data.Year);
        
        // Numeric conversion
        const numericFields = ['Year', 'Car_Age', 'Kms_Driven', 'Engine', 'Power', 'Efficiency', 'Seats', 'Present_Price', 'Owner'];
        numericFields.forEach(f => data[f] = parseFloat(data[f]));

        try {
            const response = await fetch('http://127.0.0.1:5000/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            
            const price = parseFloat(result.predicted_price);
            results.price.textContent = `₹${price.toFixed(2)} Lakhs`;
            
            const low = price * 0.95;
            const high = price * 1.05;
            results.range.textContent = `Range: ₹${low.toFixed(1)}L – ₹${high.toFixed(1)}L`;

            states.default.classList.add('hidden');
            states.success.classList.remove('hidden');

        } catch (err) {
            alert("Error connecting to prediction server.");
        } finally {
            predictBtn.disabled = false;
            predictBtn.textContent = '🚗 Predict Price';
        }
    });

    // FAQ Toggle simple interaction
    document.querySelectorAll('.faq-header').forEach(header => {
        header.addEventListener('click', () => {
            alert("This is a demo FAQ item.");
        });
    });
});
