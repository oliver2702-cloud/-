<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>超強網頁太空射擊遊戲</title>
    <style>
        body {
            margin: 0;
            background-color: #111;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            color: white;
            font-family: Arial, sans-serif;
            overflow: hidden;
        }
        canvas {
            border: 4px solid #333;
            background-color: #000;
            box-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
        }
    </style>
</head>
<body>

    <canvas id="gameCanvas" width="800" height="600"></canvas>

<script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");

    // 遊戲狀態
    let score = 0;
    let gameOver = false;

    // 1. 玩家設定
    const player = {
        x: canvas.width / 2 - 25,
        y: canvas.height - 60,
        width: 50,
        height: 40,
        speed: 7,
        color: "#00ffcc"
    };

    // 按鍵監聽
    const keys = {};
    window.addEventListener("keydown", (e) => keys[e.key] = true);
    window.addEventListener("keyup", (e) => keys[e.key] = false);

    // 2. 子彈設定
    const bullets = [];
    const bulletSpeed = 10;

    // 限制射擊頻率
    let lastShotTime = 0;
    const shootCooldown = 200; // 毫秒

    function fireBullet() {
        const currentTime = Date.now();
        if (currentTime - lastShotTime > shootCooldown) {
            bullets.push({
                x: player.x + player.width / 2 - 4,
                y: player.y,
                width: 8,
                height: 15,
                color: "#ff0055"
            });
            lastShotTime = currentTime;
        }
    }

    // 3. 敵人設定
    const enemies = [];
    const enemySpeed = 3;
    let spawnTimer = 0;

    function spawnEnemy() {
        const size = Math.random() * (50 - 30) + 30; // 隨機大小
        enemies.push({
            x: Math.random() * (canvas.width - size),
            y: -size,
            width: size,
            height: size,
            color: `hsl(${Math.random() * 360}, 100%, 60%)` // 隨機顏色
        });
    }

    // 4. 碰撞偵測函式
    function checkCollision(rect1, rect2) {
        return rect1.x < rect2.x + rect2.width &&
               rect1.x + rect1.width > rect2.x &&
               rect1.y < rect2.y + rect2.height &&
               rect1.y + rect1.height > rect2.y;
    }

    // 5. 核心遊戲循環
    function update() {
        if (gameOver) return;

        // 玩家移動控制
        if (keys["ArrowLeft"] && player.x > 0) player.x -= player.speed;
        if (keys["ArrowRight"] && player.x < canvas.width - player.width) player.x += player.speed;
        if (keys[" "]) fireBullet(); // 空白鍵射擊

        // 更新子彈位置
        for (let i = bullets.length - 1; i >= 0; i--) {
            bullets[i].y -= bulletSpeed;
            if (bullets[i].y < 0) bullets.splice(i, 1); // 飛出螢幕就刪除
        }

        // 生成敵人
        spawnTimer++;
        if (spawnTimer % 40 === 0) { // 每40影格生成一隻
            spawnEnemy();
        }

        // 更新敵人位置與碰撞偵測
        for (let i = enemies.length - 1; i >= 0; i--) {
            enemies[i].y += enemySpeed;

            // 敵人落到底部
            if (enemies[i].y > canvas.height) {
                enemies.splice(i, 1);
                continue;
            }

            // 檢查是否撞到玩家
            if (checkCollision(player, enemies[i])) {
                gameOver = true;
            }

            // 檢查是否被子彈打中
            for (let j = bullets.length - 1; j >= 0; j--) {
                if (checkCollision(bullets[j], enemies[i])) {
                    enemies.splice(i, 1);
                    bullets.splice(j, 1);
                    score += 10;
                    break;
                }
            }
        }
    }

    // 6. 畫面渲染
    function draw() {
        // 清空畫布
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // 畫玩家 (三角形戰機)
        ctx.fillStyle = player.color;
        ctx.beginPath();
        ctx.moveTo(player.x + player.width / 2, player.y);
        ctx.lineTo(player.x, player.y + player.height);
        ctx.lineTo(player.x + player.width, player.y + player.height);
        ctx.closePath();
        ctx.fill();

        // 畫子彈
        bullets.forEach(bullet => {
            ctx.fillStyle = bullet.color;
            ctx.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
        });

        // 畫敵人
        enemies.forEach(enemy => {
            ctx.fillStyle = enemy.color;
            ctx.fillRect(enemy.x, enemy.y, enemy.width, enemy.height);
        });

        // 畫分數
        ctx.fillStyle = "#fff";
        ctx.font = "20px Arial";
        ctx.fillText(`SCORE: ${score}`, 20, 40);

        // 畫遊戲結束畫面
        if (gameOver) {
            ctx.fillStyle = "rgba(0, 0, 0, 0.7)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            ctx.fillStyle = "#ff0055";
            ctx.font = "50px Arial";
            ctx.textAlign = "center";
            ctx.fillText("GAME OVER", canvas.width / 2, canvas.height / 2);
            
            ctx.fillStyle = "#fff";
            ctx.font = "20px Arial";
            ctx.fillText("重新整理網頁以再次挑戰", canvas.width / 2, canvas.height / 2 + 50);
        }
    }

    // 啟動遊戲循環
    function gameLoop() {
        update();
        draw();
        requestAnimationFrame(gameLoop);
    }

    gameLoop();
</script>

</body>
</html>