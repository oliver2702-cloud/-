import streamlit as st
import streamlit.components.v1 as components

# 1. Streamlit 網頁基本配置
st.set_page_config(page_title="太空微粒射擊遊戲", layout="centered")
st.title("🚀 極限優化：太空微粒射擊")
st.write("操作說明：使用鍵盤 **左右方向鍵 (← / →)** 或 **A / D 鍵** 移動，**空白鍵 (Space)** 發射子彈。")

# 2. 核心網頁與遊戲邏輯 (包裝於 Python 字串中，避免編譯語法衝突)
game_html = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            margin: 0;
            background-color: #050508;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            color: white;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            overflow: hidden;
        }
        #gameContainer {
            position: relative;
            box-shadow: 0 0 40px rgba(0, 150, 255, 0.25);
            border-radius: 8px;
            overflow: hidden;
        }
        canvas {
            display: block;
            background: radial-gradient(circle, #10101c 0%, #050508 100%);
        }
    </style>
</head>
<body>

    <div id="gameContainer">
        <canvas id="gameCanvas" width="800" height="550"></canvas>
    </div>

<script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");

    // 遊戲狀態控制
    let score = 0;
    let combo = 0;
    let comboTimer = 0;
    let gameOver = false;
    let gameTime = 0;

    // 優化1：動態物理學移動 (加入速度向量、摩擦力與傾斜度)
    const player = {
        x: canvas.width / 2 - 25,
        y: canvas.height - 80,
        width: 50,
        height: 40,
        vx: 0,          // X 軸速度
        maxSpeed: 8,
        friction: 0.85, // 摩擦力 (創造滑行流暢感)
        accel: 1.2,     // 加速度
        tilt: 0,        // 飛船傾斜角度
        color: "#00f0ff"
    };

    // 精確按鍵監聽系統 (兼顧左右鍵、AD鍵，並阻斷網頁原生捲軸干擾)
    const keys = {};
    window.addEventListener("keydown", (e) => {
        keys[e.key] = true;
        // 阻止瀏覽器在按下方向鍵或空白鍵時向下滾動
        if(["Space", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(e.code) || e.key === " ") {
            e.preventDefault();
        }
    });
    window.addEventListener("keyup", (e) => keys[e.key] = false);

    // 實體容器
    const bullets = [];
    const enemies = [];
    const particles = []; // 爆炸碎片微粒系統
    let lastShotTime = 0;
    const shootCooldown = 120; // 射擊極速冷卻 (毫秒)

    // 優化2：粒子特效系統 (視覺最大優化)
    function createExplosion(x, y, color) {
        const count = 15 + Math.random() * 10;
        for (let i = 0; i < count; i++) {
            const angle = Math.random() * Math.PI * 2;
            const speed = Math.random() * 4 + 2;
            particles.push({
                x: x,
                y: y,
                vx: Math.cos(angle) * speed,
                vy: Math.sin(angle) * speed,
                radius: Math.random() * 2.5 + 1,
                alpha: 1,
                decay: Math.random() * 0.02 + 0.015,
                color: color
            });
        }
    }

    // 動態難度敵人生成
    function spawnEnemy() {
        const size = Math.random() * (45 - 25) + 25;
        const speedFactor = 1 + (gameTime / 2500); // 隨時間線性微調變快
        enemies.push({
            x: Math.random() * (canvas.width - size),
            y: -size,
            width: size,
            height: size,
            vy: (Math.random() * 1.5 + 2.5) * speedFactor,
            vx: (Math.random() - 0.5) * 1.5, // 敵機具備微幅左右飄移 A.I.
            color: `hsl(${Math.random() * 35 + 345}, 100%, 65%)`, // 熾熱火系色調
            hp: size > 38 ? 2 : 1 // 體型較大的方塊需要擊中兩次
        });
    }

    // 標準矩形碰撞偵測
    function checkCollision(rect1, rect2) {
        return rect1.x < rect2.x + rect2.width &&
               rect1.x + rect1.width > rect2.x &&
               rect1.y < rect2.y + rect2.height &&
               rect1.y + rect1.height > rect2.y;
    }

    // 3. 物理與邏輯更新循環
    function update() {
        if (gameOver) return;
        gameTime++;

        // 監聽左右鍵與 AD 鍵，賦予加速度
        if (keys["ArrowLeft"] || keys["a"] || keys["A"]) player.vx -= player.accel;
        if (keys["ArrowRight"] || keys["d"] || keys["D"]) player.vx += player.accel;
        
        // 套用物理摩擦力與速度限制
        player.vx *= player.friction;
        player.x += player.vx;
        
        // 邊界防禦線
        if (player.x < 0) { player.x = 0; player.vx = 0; }
        if (player.x > canvas.width - player.width) { player.x = canvas.width - player.width; player.vx = 0; }

        // 動態視覺計算：根據當前移動速度決定戰機傾斜幅度
        player.tilt = player.vx * 0.035;

        // 連擊系統動態射擊 (Combo 達 10 以上解鎖三連發散射)
        if (keys[" "] || keys["Enter"]) {
            const currentTime = Date.now();
            if (currentTime - lastShotTime > shootCooldown) {
                const bulletX = player.x + player.width / 2;
                if (combo >= 10) {
                    bullets.push({ x: bulletX - 15, y: player.y, vx: -1.8, vy: -12, color: "#ffff00" });
                    bullets.push({ x: bulletX - 3,  y: player.y, vx: 0,    vy: -14, color: "#00f0ff" });
                    bullets.push({ x: bulletX + 9,  y: player.y, vx: 1.8,  vy: -12, color: "#ffff00" });
                } else {
                    bullets.push({ x: bulletX - 10, y: player.y, vx: 0, vy: -12, color: "#00f0ff" });
                    bullets.push({ x: bulletX + 6,  y: player.y, vx: 0, vy: -12, color: "#00f0ff" });
                }
                lastShotTime = currentTime;
            }
        }

        // 處理子彈移動與極限優化（過期記憶體回收）
        for (let i = bullets.length - 1; i >= 0; i--) {
            bullets[i].x += bullets[i].vx;
            bullets[i].y += bullets[i].vy;
            if (bullets[i].y < -20 || bullets[i].x < -10 || bullets[i].x > canvas.width + 10) {
                bullets.splice(i, 1);
            }
        }

        // 連擊計時衰減
        if (combo > 0) {
            comboTimer--;
            if (comboTimer <= 0) combo = 0;
        }

        // 動態生成敵人頻率控制
        const spawnRate = Math.max(12, 32 - Math.floor(gameTime / 350));
        if (gameTime % spawnRate === 0) spawnEnemy();

        // 處理敵人移動與碰撞邏輯
        for (let i = enemies.length - 1; i >= 0; i--) {
            enemies[i].x += enemies[i].vx;
            enemies[i].y += enemies[i].vy;

            // 敵機碰撞邊緣時反彈
            if (enemies[i].x < 0 || enemies[i].x > canvas.width - enemies[i].width) enemies[i].vx *= -1;

            // 敵機漏接
            if (enemies[i].y > canvas.height) {
                enemies.splice(i, 1);
                combo = 0; // 漏怪會直接中斷 Combo 
                continue;
            }

            // 玩家與敵機相撞
            if (checkCollision(player, enemies[i])) {
                createExplosion(player.x + player.width/2, player.y + player.height/2, player.color);
                createExplosion(enemies[i].x + enemies[i].width/2, enemies[i].y + enemies[i].height/2, enemies[i].color);
                gameOver = true;
            }

            // 子彈與敵機碰撞
            for (let j = bullets.length - 1; j >= 0; j--) {
                const b = { x: bullets[j].x, y: bullets[j].y, width: 6, height: 12 };
                if (checkCollision(b, enemies[i])) {
                    enemies[i].hp--;
                    bullets.splice(j, 1);

                    if (enemies[i].hp <= 0) {
                        createExplosion(enemies[i].x + enemies[i].width/2, enemies[i].y + enemies[i].height/2, enemies[i].color);
                        combo++;
                        comboTimer = 150; // 2.5秒內必須再次擊殺
                        score += 10 * (1 + Math.floor(combo / 5)); // 帶有 Combo 權重的計分公式
                        enemies.splice(i, 1);
                    }
                    break;
                }
            }
        }

        // 更新爆炸微粒生命週期
        for (let i = particles.length - 1; i >= 0; i--) {
            particles[i].x += particles[i].vx;
            particles[i].y += particles[i].vy;
            particles[i].alpha -= particles[i].decay;
            if (particles[i].alpha <= 0) {
                particles.splice(i, 1);
            }
        }
    }

    // 4. 高階圖形發光渲染 (Bloom Filter Effect)
    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // 背景動態繁星特效 (多層次速度感)
        ctx.fillStyle = "rgba(255, 255, 255, 0.15)";
        for (let i = 0; i < 20; i++) {
            let starY = (gameTime * (1 + (i % 2))) % canvas.height;
            let starX = (i * 41) % canvas.width;
            ctx.fillRect(starX, starY, 2, 2);
        }

        // 開啟全螢幕霓虹發光濾鏡 (超強視覺關鍵)
        ctx.shadowBlur = 10;

        // 渲染玩家 (進行平移轉動矩陣操作，實現平滑傾斜)
        ctx.save();
        ctx.translate(player.x + player.width / 2, player.y + player.height / 2);
        ctx.rotate(player.tilt);
        
        // 後置粒子引擎噴火特效
        ctx.shadowColor = "#ffaa00";
        ctx.fillStyle = gameTime % 2 === 0 ? "#ff5500" : "#ff9900";
        ctx.beginPath();
        ctx.moveTo(-8, player.height / 2);
        ctx.lineTo(0, player.height / 2 + (12 + Math.random() * 8));
        ctx.lineTo(8, player.height / 2);
        ctx.closePath();
        ctx.fill();

        // 繪製戰機本體
        ctx.shadowColor = player.color;
        ctx.fillStyle = player.color;
        ctx.beginPath();
        ctx.moveTo(0, -player.height / 2);
        ctx.lineTo(-player.width / 2, player.height / 2);
        ctx.lineTo(player.width / 2, player.height / 2);
        ctx.closePath();
        ctx.fill();
        ctx.restore();

        // 渲染子彈
        bullets.forEach(b => {
            ctx.shadowColor = b.color;
            ctx.fillStyle = b.color;
            ctx.fillRect(b.x, b.y, 6, 12);
        });

        // 渲染敵方目標
        enemies.forEach(e => {
            ctx.shadowColor = e.color;
            ctx.fillStyle = e.color;
            ctx.fillRect(e.x, e.y, e.width, e.height);
            if (e.hp > 1) { // 大型強固敵機加上核心裝甲框
                ctx.lineWidth = 2;
                ctx.strokeStyle = "#fff";
                ctx.strokeRect(e.x + 4, e.y + 4, e.width - 8, e.height - 8);
            }
        });

        // 渲染粒子 (渲染微粒時關閉發光濾鏡以將效能最大化，避免幀率下跌)
        ctx.shadowBlur = 0;
        particles.forEach(p => {
            ctx.save();
            ctx.globalAlpha = p.alpha;
            ctx.fillStyle = p.color;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();
        });

        // 繪製 UI HUD 數據介面
        ctx.fillStyle = "#fff";
        ctx.font = "bold 20px 'Segoe UI', Arial";
        ctx.fillText(`SCORE: ${score}`, 25, 40);

        if (combo >= 5) {
            ctx.fillStyle = `hsl(${gameTime % 360}, 100%, 70%)`;
            ctx.font = "italic bold 24px 'Segoe UI'";
            ctx.fillText(`${combo} COMBO!`, 25, 75);
            
            // 繪製 Combo 的倒數計時條
            ctx.fillStyle = "rgba(255,255,255,0.15)";
            ctx.fillRect(25, 90, 140, 5);
            ctx.fillStyle = `hsl(${gameTime % 360}, 100%, 70%)`;
            ctx.fillRect(25, 90, (comboTimer / 150) * 140, 5);
        }

        ctx.fillStyle = combo >= 10 ? "#ffff00" : "#00f0ff";
        ctx.font = "13px Arial";
        ctx.fillText(`WEAPON SYSTEM: ${combo >= 10 ? "MAX HYPER (三連發)" : "STANDARD (雙線)"}`, 25, canvas.height - 25);

        // 遊戲結束終點畫面
        if (gameOver) {
            ctx.fillStyle = "rgba(5, 5, 10, 0.85)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            ctx.shadowBlur = 20;
            ctx.shadowColor = "#ff0055";
            ctx.fillStyle = "#ff0055";
            ctx.font = "bold 55px 'Segoe UI'";
            ctx.textAlign = "center";
            ctx.fillText("MISSION FAILED", canvas.width / 2, canvas.height / 2 - 20);
            
            ctx.shadowBlur = 0;
            ctx.fillStyle = "#fff";
            ctx.font = "22px 'Segoe UI'";
            ctx.fillText(`最終作戰得分: ${score}`, canvas.width / 2, canvas.height / 2 + 35);
            ctx.font = "15px Arial";
            ctx.fillStyle = "#777";
            ctx.fillText("點擊畫面上方 Streamlit 的 Rerun 或重整網頁以重啟戰機", canvas.width / 2, canvas.height / 2 + 85);
        }
    }

    // 5. 執行核心硬體級循環偵 (60FPS 高流暢維持)
    function gameLoop() {
        update();
        draw();
        requestAnimationFrame(gameLoop);
    }

    gameLoop();
</script>
</body>
</html>
"""

# 3. 使用 Streamlit 元件安全引入（高寬與 Canvas 完美契合，消除滾動條）
components.html(game_html, height=580, width=820)