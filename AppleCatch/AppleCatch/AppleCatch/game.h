#pragma once
#include <SFML/Graphics.hpp>
#include <SFML/audio.hpp>
#include <vector>
#include <iostream>
using namespace sf;

class Game
{
public:
	Game();
	int score, lives, spawnInterval;
	float dt, multiplier, appleMultiplier, fallSpeed;
	Clock clock, appleClock, gameTime;
	Text displayTime, displayScore, displayLives;
	Texture backgroundTexture;
	Sprite backgroundSprite, playerSprite;
	Sound collect, lifeUp, explosion, missedApple, missedHeart;
	std::vector<std::pair<Sprite, int>> apples;
	RectangleShape playerHitbox;
	void spawnApple();
	~Game();
private:
	Font font;
	Texture appleTexture, bombTexture, heartTexture, playerTexture;
	SoundBuffer collectBuffer, heartBuffer, explosionBuffer, missedAppleBuffer, missedHeartBuffer;
};