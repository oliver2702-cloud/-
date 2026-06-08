import streamlit as st
import streamlit.components.v1 as components

# 設定網頁標題與佈局
st.set_page_config(page_title="太空射擊遊戲", layout="centered")
st.title("🚀 極限優化：太空微粒射擊遊戲")
st.write("使用左右方向鍵（或 A/D 鍵）移動，空白鍵（Space）發射子彈！")

# 將完整的前端網頁程式碼包裝在 Python 字串中
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
            box-shadow: 0 0 50px rgba(0, 150, 255, 0.3);
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

    let score = 0;
    let combo = 0;
    let comboTimer = 0;
    let gameOver = false;
    let gameTime = 0;

    const player = {
        x: canvas.width / 2 - 25,
        y: canvas.height - 80,
        width: 50,
        height: 40,
        vx: 0,
        maxSpeed: 8,
        friction: 0.85,
        accel: 1.2,
        tilt: 0,
        color: "#00f0ff"
    };

    const keys = {};
    window.addEventListener("keydown", (e) => {
        keys[e.key] = true;
        // 防止網頁捲軸因為空白鍵或方向鍵而滾動
        if(["Space", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(e.code)) {
            e.preventDefault();
        }
    });
    window.addEventListener("keyup", (e) => keys[e.key] = false);

    const bullets = [];
    const enemies = [];
    const particles = [];
    let lastShotTime = 0;
    const shootCooldown = 120;

    function createExplosion(x, y, color) {
        const count = 20 + Math.random() * 15;
        for (let i = 0; i < count; i++) {
            const angle = Math.random() * Math.PI * 2;
            const speed = Math.random() * 5 + 2;
            particles.push({
                x: x,
                y: y,
                vx: Math.cos(angle) * speed,
                vy: Math.sin(angle) * speed,
                radius: Math.random() * 3 + 1,
                alpha: 1,
                decay: Math.random() * 0.02 + 0.015,
                color: color
            });
        }
    }

    function spawnEnemy() {
        const size = Math.random() * (45 - 25) + 25;
        const speedFactor = 1 + (gameTime / 2000);
        enemies.push({
            x: Math.random() * (canvas.width - size),
            y: -size,
            width: size,
            height: size,
            vy: (Math.random() * 2 + 2) * speedFactor,
            vx: (Math.random() - 0.5) * 2,
            color: `hsl(${Math.random() * 40 + 340}, 100%, 60%)`,
            hp: size > 38 ? 2 : 1
        });
    }

    function checkCollision(rect1, rect2) {
        return rect1.x < rect2.x + rect2.width &&
               rect1.x + rect1.width > rect2.x &&
               rect1.y < rect2.y + rect2.height &&
               rect1.y + rect1.height > rect2.y;
    }

    function update() {
        if (gameOver) return;
        gameTime++;

        if (keys["ArrowLeft"] || keys["a"]) player.vx -= player.accel;
        if (keys["ArrowRight"] || keys["d"]) player.vx += player.accel;
        
        player.vx *= player.friction;
        player.x += player.vx;
        if (player.x < 0) { player.x = 0; player.vx = 0; }
        if (player.x > canvas.width - player.width) { player.x = canvas.width - player.width; player.vx = 0; }

        player.tilt = player.vx * 0.03;

        if (keys[" "] || keys["Enter"]) {
            const currentTime = Date.now();
            if (currentTime - lastShotTime > shootCooldown) {
                const bulletX = player.x + player.width / 2;
                if (combo >= 10) {
                    bullets.push({ x: bulletX - 15, y: player.y, vx: -2, vy: -12, color: "#ffff00" });
                    bullets.push({ x: bulletX - 3,  y: player.y, vx: 0,  vy: -14, color: "#00f0ff" });
                    bullets.push({ x: bulletX + 9,  y: player.y, vx: 2,  vy: -12, color: "#ffff00" });
                } else {
                    bullets.push({ x: bulletX - 10, y: player.y, vx: 0, vy: -12, color: "#00f0ff" });
                    bullets.push({ x: bulletX + 6,  y: player.y, vx: 0, vy: -12, color: "#00f0ff" });
                }
                lastShotTime = currentTime;
            }
        }

        for (let i = bullets.length - 1; i >= 0; i--) {
            bullets[i].x += bullets[i].vx;
            bullets[i].y += bullets[i].vy;
            if (bullets[i].y < -20 || bullets[i].x < 0 || bullets[i].x > canvas.width) {
                bullets.splice(i, 1);
            }
        }

        if (combo > 0) {
            comboTimer--;
            if (comboTimer <= 0) combo = 0;
        }

        const spawnRate = Math.max(15, 35 - Math.floor(gameTime / 300));
        if (gameTime % spawnRate === 0) spawnEnemy();

        for (let i = enemies.length - 1; i >= 0; i--) {
            enemies[i].x += enemies[i].vx;
            enemies[i].y += enemies[i].vy;

            if (enemies[i].x < 0 || enemies[i].x > canvas.width - enemies[i].width) enemies[i].vx *= -1;

            if (enemies[i].y > canvas.height) {
                enemies.splice(i, 1);
                combo = 0;
                continue;
            }

            if (checkCollision(player, enemies[i])) {
                createExplosion(player.x + player.width/2, player.y + player.height/2, player.color);
                createExplosion(enemies[i].x + enemies[i].width/2, enemies[i].y + enemies[i].height/2, enemies[i].color);
                gameOver = true;
            }

            for (let j = bullets.length - 1; j >= 0; j--) {
                const b = { x: bullets[j].x, y: bullets[j].y, width: 6, height: 12 };
                if (checkCollision(b, enemies[i])) {
                    enemies[i].hp--;
                    bullets.splice(j, 1);

                    if (enemies[i].hp <= 0) {
                        createExplosion(enemies[i].x + enemies[i].width/2, enemies[i].y + enemies[i].height/2, enemies[i].color);
                        combo++;
                        comboTimer = 180;
                        score += 10 * (1 + Math.floor(combo / 5));
                        enemies.splice(i, 1);
                    }
                    break;
                }
            }
        }

        for (let i = particles.length - 1; i >= 0; i--) {
            particles[i].x += particles[i].vx;
            particles[i].y += particles[i].vy;
            particles[i].alpha -= particles[i].decay;
            if (particles[i].alpha <= 0) {
                particles.splice(i, 1);
            }
        }
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = "rgba(255, 255, 255, 0.2)";
        for (let i = 0; i < 20; i++) {
            let starY = (gameTime * (1 + (i % 3))) % canvas.height;
            let starX = (i * 47) % canvas.width;
            ctx.fillRect(starX, starY, 2, 2);
        }

        ctx.shadowBlur = 12;

        ctx.save();
        ctx.translate(player.x + player.width / 2, player.y + player.height / 2);
        ctx.rotate(player.tilt);
        
        ctx.shadowColor = "#ffaa00";
        ctx.fillStyle = gameTime % 2 === 0 ? "#ff5500" : "#ffaa00";
        ctx.beginPath();
        ctx.moveTo(-10, player.height / 2);
        ctx.lineTo(0, player.height / 2 + (15 + Math.random() * 10));
        ctx.lineTo(10, player.height / 2);
        ctx.closePath();
        ctx.fill();

        ctx.shadowColor = player.color;
        ctx.fillStyle = player.color;
        ctx.beginPath();
        ctx.moveTo(0, -player.height / 2);
        ctx.lineTo(-player.width / 2, player.height / 2);
        ctx.lineTo(player.width / 2, player.height / 2);
        ctx.closePath();
        ctx.fill();
        ctx.restore();

        bullets.forEach(b => {
            ctx.shadowColor = b.color;
            ctx.fillStyle = b.color;
            ctx.fillRect(b.x, b.y, 6, 12);
        });

        enemies.forEach(e => {
            ctx.shadowColor = e.color;
            ctx.fillStyle = e.color;
            ctx.lineWidth = 2;
            ctx.strokeStyle = "#fff";
            ctx.fillRect(e.x, e.y, e.width, e.height);
            if (e.hp > 1) {
                ctx.strokeRect(e.x + 4, e.y + 4, e.width - 8, e.height - 8);
            }
        });

        particles.forEach(p => {
            ctx.shadowBlur = 0;
            ctx.save();
            ctx.globalAlpha = p.alpha;
            ctx.fillStyle = p.color;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();
        });

        ctx.shadowBlur = 0;

        ctx.fillStyle = "#fff";
        ctx.font = "bold 22px 'Segoe UI'";
        ctx.fillText(`SCORE: ${score}`, 25, 40);

        if (combo >= 5) {
            ctx.fillStyle = `hsl(${gameTime % 360}, 100%, 70%)`;
            ctx.font = "italic bold 26px 'Segoe UI'";
            ctx.fillText(`${combo} COMBO!`, 25, 80);
            
            ctx.fillStyle = "rgba(255,255,255,0.2)";
            ctx.fillRect(25, 95, 150, 6);
            ctx.fillStyle = `hsl(${gameTime % 360}, 100%, 70%)`;
            ctx.fillRect(25, 95, (comboTimer / 180) * 150, 6);
        }

        ctx.fillStyle = combo >= 10 ? "#ffff00" : "#00f0ff";
        ctx.font = "14px Arial";
        ctx.fillText(`WEAPON LEVEL: ${combo >= 10 ? "MAX (三連發)" : "LV1 (雙線)"}`, 25, canvas.height - 25);

        if (gameOver) {
            ctx.fillStyle = "rgba(5, 5, 10, 0.85)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            ctx.shadowBlur = 20;
            ctx.shadowColor = "#ff0055";
            ctx.fillStyle = "#ff0055";
            ctx.font = "bold 60px 'Segoe UI'";
            ctx.textAlign = "center";
            ctx.fillText("MISSION FAILED", canvas.width / 2, canvas.height / 2 - 20);
            
            ctx.shadowBlur = 0;
            ctx.fillStyle = "#fff";
            ctx.font = "24px 'Segoe UI'";
            ctx.fillText(`最終得分: ${score}`, canvas.width / 2, canvas.height / 2 + 40);
            ctx.font = "16px Arial";
            ctx.fillStyle = "#888";
            ctx.fillText("重新整理網頁以再次挑戰", canvas.width / 2, canvas.height / 2 + 90);
        }
    }

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

# 在 Streamlit 中安全渲染組件 (設定足夠的高寬)
components.html(game_html, height=600, width=850)