const refreshBtn = document.getElementById('refreshBtn');
const status = document.getElementById('status');

refreshBtn.addEventListener('click', () => {
    status.textContent = 'در حال بروزرسانی ...';
    fetch('/update')
        .then(response => response.json())
        .then(data => {
            document.getElementById('date').textContent = `تاریخ و زمان: ${data.date}`;
            document.getElementById('gold_mesghal').textContent = data.gold_mesghal;
            document.getElementById('gold_18').textContent = data.gold_18;
            document.getElementById('gold_24').textContent = data.gold_24;
            document.getElementById('new_coin').textContent = data.new_coin;
            document.getElementById('old_coin').textContent = data.old_coin;
            document.getElementById('half_coin').textContent = data.half_coin;
            document.getElementById('tether').textContent = data.tether;
            document.getElementById('dollar').textContent = data.dollar;
            document.getElementById('euro').textContent = data.euro;
            document.getElementById('btc').textContent = data.btc;
            document.getElementById('eth').textContent = data.eth;
            status.textContent = '✅ بروزرسانی با موفقیت انجام شد';
        })
        .catch(err => {
            console.error(err);
            status.textContent = '❌ خطا در بروزرسانی';
        });
});
