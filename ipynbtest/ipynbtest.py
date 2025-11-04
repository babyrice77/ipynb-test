import React, { useState, useEffect, useRef } from 'react';

const SuperMarioGame = () => {
  const canvasRef = useRef(null);
  const [score, setScore] = useState(0);
  const [gameOver, setGameOver] = useState(false);
  const [gameStarted, setGameStarted] = useState(false);
  
  const gameStateRef = useRef({
    player: {
      x: 100,
      y: 300,
      width: 32,
      height: 32,
      velocityY: 0,
      velocityX: 0,
      jumping: false,
      direction: 1
    },
    platforms: [
      { x: 0, y: 400, width: 800, height: 20 },
      { x: 200, y: 320, width: 120, height: 20 },
      { x: 400, y: 250, width: 120, height: 20 },
      { x: 600, y: 180, width: 120, height: 20 },
      { x: 100, y: 180, width: 100, height: 20 }
    ],
    coins: [
      { x: 250, y: 280, collected: false },
      { x: 450, y: 210, collected: false },
      { x: 650, y: 140, collected: false },
      { x: 150, y: 140, collected: false },
      { x: 350, y: 350, collected: false }
    ],
    enemies: [
      { x: 300, y: 290, width: 30, height: 30, velocityX: 2, direction: 1 },
      { x: 500, y: 220, width: 30, height: 30, velocityX: 2, direction: 1 }
    ],
    keys: {},
    gravity: 0.6,
    jumpStrength: -13,
    moveSpeed: 5,
    score: 0
  });

  useEffect(() => {
    if (!gameStarted) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const game = gameStateRef.current;

    const handleKeyDown = (e) => {
      game.keys[e.key] = true;
      if (e.key === ' ' && !game.player.jumping) {
        game.player.velocityY = game.jumpStrength;
        game.player.jumping = true;
      }
    };

    const handleKeyUp = (e) => {
      game.keys[e.key] = false;
    };

    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);

    const gameLoop = () => {
      if (gameOver) return;

      // Clear canvas
      ctx.fillStyle = '#5c94fc';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Draw clouds
      ctx.fillStyle = 'white';
      ctx.fillRect(100, 50, 60, 30);
      ctx.fillRect(110, 40, 40, 20);
      ctx.fillRect(400, 80, 60, 30);
      ctx.fillRect(410, 70, 40, 20);

      // Player movement
      if (game.keys['ArrowLeft'] || game.keys['a']) {
        game.player.velocityX = -game.moveSpeed;
        game.player.direction = -1;
      } else if (game.keys['ArrowRight'] || game.keys['d']) {
        game.player.velocityX = game.moveSpeed;
        game.player.direction = 1;
      } else {
        game.player.velocityX = 0;
      }

      game.player.x += game.player.velocityX;
      game.player.velocityY += game.gravity;
      game.player.y += game.player.velocityY;

      // Platform collision
      game.player.jumping = true;
      game.platforms.forEach(platform => {
        if (
          game.player.x < platform.x + platform.width &&
          game.player.x + game.player.width > platform.x &&
          game.player.y + game.player.height > platform.y &&
          game.player.y + game.player.height < platform.y + platform.height &&
          game.player.velocityY > 0
        ) {
          game.player.y = platform.y - game.player.height;
          game.player.velocityY = 0;
          game.player.jumping = false;
        }
      });

      // Boundaries
      if (game.player.x < 0) game.player.x = 0;
      if (game.player.x + game.player.width > canvas.width) {
        game.player.x = canvas.width - game.player.width;
      }

      // Game over if fall
      if (game.player.y > canvas.height) {
        setGameOver(true);
        return;
      }

      // Draw platforms
      ctx.fillStyle = '#8B4513';
      game.platforms.forEach(platform => {
        ctx.fillRect(platform.x, platform.y, platform.width, platform.height);
        ctx.fillStyle = '#654321';
        for (let i = 0; i < platform.width; i += 20) {
          ctx.fillRect(platform.x + i, platform.y, 18, 18);
        }
        ctx.fillStyle = '#8B4513';
      });

      // Draw and collect coins
      game.coins.forEach(coin => {
        if (!coin.collected) {
          if (
            game.player.x < coin.x + 20 &&
            game.player.x + game.player.width > coin.x &&
            game.player.y < coin.y + 20 &&
            game.player.y + game.player.height > coin.y
          ) {
            coin.collected = true;
            game.score += 10;
            setScore(game.score);
          } else {
            ctx.fillStyle = '#FFD700';
            ctx.beginPath();
            ctx.arc(coin.x + 10, coin.y + 10, 10, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = '#FFA500';
            ctx.beginPath();
            ctx.arc(coin.x + 10, coin.y + 10, 6, 0, Math.PI * 2);
            ctx.fill();
          }
        }
      });

      // Update and draw enemies
      game.enemies.forEach((enemy, index) => {
        enemy.x += enemy.velocityX * enemy.direction;
        
        // Enemy platform boundaries
        let onPlatform = false;
        game.platforms.forEach(platform => {
          if (
            enemy.y + enemy.height >= platform.y &&
            enemy.y + enemy.height <= platform.y + platform.height
          ) {
            if (enemy.x <= platform.x || enemy.x + enemy.width >= platform.x + platform.width) {
              enemy.direction *= -1;
            }
            onPlatform = true;
          }
        });

        // Check collision with player
        if (
          game.player.x < enemy.x + enemy.width &&
          game.player.x + game.player.width > enemy.x &&
          game.player.y < enemy.y + enemy.height &&
          game.player.y + game.player.height > enemy.y
        ) {
          // Player jumps on enemy
          if (game.player.velocityY > 0 && game.player.y + game.player.height - 10 < enemy.y) {
            game.enemies.splice(index, 1);
            game.player.velocityY = -8;
            game.score += 20;
            setScore(game.score);
          } else {
            setGameOver(true);
            return;
          }
        }

        // Draw enemy
        ctx.fillStyle = '#8B0000';
        ctx.fillRect(enemy.x, enemy.y, enemy.width, enemy.height);
        ctx.fillStyle = '#FF0000';
        ctx.fillRect(enemy.x + 5, enemy.y + 5, enemy.width - 10, enemy.height - 10);
        // Eyes
        ctx.fillStyle = 'white';
        ctx.fillRect(enemy.x + 8, enemy.y + 8, 6, 6);
        ctx.fillRect(enemy.x + 16, enemy.y + 8, 6, 6);
        ctx.fillStyle = 'black';
        ctx.fillRect(enemy.x + 10, enemy.y + 10, 3, 3);
        ctx.fillRect(enemy.x + 18, enemy.y + 10, 3, 3);
      });

      // Draw player
      ctx.fillStyle = '#FF0000';
      ctx.fillRect(game.player.x, game.player.y, game.player.width, game.player.height);
      
      // Mario hat
      ctx.fillRect(game.player.x + 4, game.player.y - 8, 24, 8);
      
      // Face
      ctx.fillStyle = '#FFD4A3';
      ctx.fillRect(game.player.x + 8, game.player.y + 8, 16, 12);
      
      // Eyes
      ctx.fillStyle = 'black';
      const eyeOffset = game.player.direction > 0 ? 2 : -2;
      ctx.fillRect(game.player.x + 12 + eyeOffset, game.player.y + 12, 3, 3);
      ctx.fillRect(game.player.x + 18 + eyeOffset, game.player.y + 12, 3, 3);
      
      // Overalls
      ctx.fillStyle = '#0000FF';
      ctx.fillRect(game.player.x + 6, game.player.y + 20, 20, 12);

      requestAnimationFrame(gameLoop);
    };

    gameLoop();

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
    };
  }, [gameStarted, gameOver]);

  const startGame = () => {
    setGameStarted(true);
    setGameOver(false);
    setScore(0);
    gameStateRef.current = {
      player: {
        x: 100,
        y: 300,
        width: 32,
        height: 32,
        velocityY: 0,
        velocityX: 0,
        jumping: false,
        direction: 1
      },
      platforms: [
        { x: 0, y: 400, width: 800, height: 20 },
        { x: 200, y: 320, width: 120, height: 20 },
        { x: 400, y: 250, width: 120, height: 20 },
        { x: 600, y: 180, width: 120, height: 20 },
        { x: 100, y: 180, width: 100, height: 20 }
      ],
      coins: [
        { x: 250, y: 280, collected: false },
        { x: 450, y: 210, collected: false },
        { x: 650, y: 140, collected: false },
        { x: 150, y: 140, collected: false },
        { x: 350, y: 350, collected: false }
      ],
      enemies: [
        { x: 300, y: 290, width: 30, height: 30, velocityX: 2, direction: 1 },
        { x: 500, y: 220, width: 30, height: 30, velocityX: 2, direction: 1 }
      ],
      keys: {},
      gravity: 0.6,
      jumpStrength: -13,
      moveSpeed: 5,
      score: 0
    };
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-b from-blue-400 to-blue-600 p-4">
      <div className="bg-white rounded-lg shadow-2xl p-6">
        <h1 className="text-4xl font-bold text-center mb-4 text-red-600">🍄 超级马里奥 🍄</h1>
        
        <div className="mb-4 text-center">
          <span className="text-2xl font-bold text-yellow-600">得分: {score}</span>
        </div>

        <canvas
          ref={canvasRef}
          width={800}
          height={450}
          className="border-4 border-gray-800 rounded"
        />

        <div className="mt-4 text-center">
          {!gameStarted ? (
            <button
              onClick={startGame}
              className="bg-green-500 hover:bg-green-600 text-white font-bold py-3 px-8 rounded-lg text-xl"
            >
              开始游戏
            </button>
          ) : gameOver ? (
            <div>
              <p className="text-2xl font-bold text-red-600 mb-4">游戏结束！</p>
              <button
                onClick={startGame}
                className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-3 px-8 rounded-lg text-xl"
              >
                重新开始
              </button>
            </div>
          ) : (
            <div className="text-gray-700">
              <p className="font-semibold">操作说明:</p>
              <p>← → 或 A D: 移动</p>
              <p>空格: 跳跃</p>
              <p>🎯 收集金币，踩敌人！</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SuperMarioGame;
