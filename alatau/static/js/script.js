document.addEventListener('DOMContentLoaded', () => {
    loadRooms();

    // Эффект шапки при скролле
    window.addEventListener('scroll', () => {
        const nav = document.getElementById('main-nav');
        if (window.scrollY > 50) {
            nav.classList.add('scrolled');
        } else {
            nav.classList.remove('scrolled');
        }
    });
});

async function loadRooms() {
    try {
        const res = await fetch('/api/rooms');
        const rooms = await res.json();
        const select = document.getElementById('room-select');

        select.innerHTML = rooms.map(room =>
            `<option value="${room.id}">${room.name} (${room.price.toLocaleString()} ₸ / ночь)</option>`
        ).join('');
    } catch (err) {
        console.error('Ошибка загрузки данных о номерах:', err);
    }
}

document.getElementById('booking-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const data = {
        room_id: document.getElementById('room-select').value,
        nights: document.getElementById('nights').value,
        guests: document.getElementById('guests').value
    };

    const resultDiv = document.getElementById('booking-result');

    try {
        const res = await fetch('/api/book', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await res.json();

        resultDiv.classList.remove('hidden');
        if (result.status === 'success') {
            resultDiv.className = 'mt-8 p-6 rounded-2xl bg-green-50 text-green-700 border-2 border-green-100';
            resultDiv.innerHTML = `
                <div class="text-sm uppercase tracking-widest mb-1 opacity-70">Успешно забронировано</div>
                <div class="text-2xl font-black">${result.room_name}</div>
                <div class="mt-2 text-xl">Итого: ${result.total_price.toLocaleString()} ₸</div>
            `;
        }
    } catch (err) {
        alert('Ошибка соединения с сервером');
    }
});

function openModal(id) { document.getElementById(id + '-modal').classList.remove('hidden'); }
function closeModal(id) { document.getElementById(id + '-modal').classList.add('hidden'); }

async function handleLogin() {
    const username = document.getElementById('username-input').value;
    if(!username) return;

    const res = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username })
    });

    const result = await res.json();
    if(result.status === 'success') {
        document.getElementById('user-name-display').innerText = result.username;
        closeModal('auth');
    }
}