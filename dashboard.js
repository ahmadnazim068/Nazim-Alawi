// Centralized Dashboard Data Management Controller

function fetchLiveData() {
    fetch('/api/live_data')
        .then(response => response.json())
        .then(data => {
            // 1. Team 1: Registration Updates
            document.getElementById('checkin-count').innerText = 
                `${data.team_1.checked_in}/${data.team_1.total_runners}`;

            // 2. Team 2: Top Timing Leader Metric Display
            document.getElementById('leader-time').innerText = data.team_2.leader_time;

            // 3. Team 3: Environmental Safety System Update
            document.getElementById('safety-temp').innerText = `${data.team_3.temp.toFixed(1)}°C`;
            const sosElement = document.getElementById('sos-indicator');
            if (data.team_3.sos_triggered) {
                sosElement.innerText = "⚠️ STATUS: SOS TRIGGERED";
                sosElement.style.color = "#ef233c";
            } else {
                sosElement.innerText = "⚠️ Status: Normal";
                sosElement.style.color = "#00b4d8";
            }

            // 4. Team 4: Hydration Reservoir Stations Tracker
            document.getElementById('water-level').innerText = `${data.team_4.water_level_percent}%`;

            // 5. Dynamic Injection Loop: Arc IoT Custom Array Leaderboard
            const leaderboardContainer = document.getElementById('live-leaderboard-entries');
            if (leaderboardContainer && data.team_2.runners) {
                if (data.team_2.runners.length === 0) {
                    leaderboardContainer.innerHTML = `<div style="text-align: center; color: #486581; padding: 20px;">No runner checkpoints active.</div>`;
                } else {
                    leaderboardContainer.innerHTML = ''; // Clear old layout ticks
                    data.team_2.runners.forEach((runner, index) => {
            
                    // Fallback safety checks in case keys use different naming patterns
                    let currentRunnerId = runner.runner_id || runner.id || runner.nama || `Runner #${index + 1}`;
                    let currentTime = runner.recorded_time || runner.time || "00:00:00";
                    let currentStatus = runner.status || "Checkpoint Pass Verified";

                    leaderboardContainer.innerHTML += `
                        <div class="runner-row">
                            <span class="runner-rank">#${index + 1}</span>
                            <div class="runner-info">
                                <span class="runner-name">${currentRunnerId}</span>
                                <span class="runner-matrik">${currentStatus}</span>
                            </div>
                            <span class="runner-time">${currentTime}</span>
                        </div>`;
                    });
                }
            }
        })
        .catch(error => console.error('Error fetching centralized gateway updates:', error));
}

// Global action trigger for exporting records to Excel file formats
function downloadExcelReport() {
    window.location.href = '/api/export_excel';
}

// Establish real-time execution loop interval (Pulls updates every two seconds)
setInterval(fetchLiveData, 2000);

// Run initialization trigger on DOM window initialization
document.addEventListener('DOMContentLoaded', fetchLiveData);
