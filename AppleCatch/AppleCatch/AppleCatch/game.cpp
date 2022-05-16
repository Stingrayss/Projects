#include "game.h"

Game::Game() {
	srand(time(NULL));
	//create background
	backgroundTexture.loadFromFile("Assets/background.png", IntRect(0, 0, 800, 600));
	if (!backgroundTexture.loadFromFile("Assets/background.png"))
		std::cout << "Could not load texture" << std::endl;
	backgroundSprite.setTexture(backgroundTexture);

	//create player sprite (not the actual hitbox)
	playerTexture.loadFromFile("Assets/guy.png", IntRect(400, 500, 32, 32));
	if (!playerTexture.loadFromFile("Assets/guy.png"))
		std::cout << "Could not load texture" << std::endl;
	playerSprite.setTexture(playerTexture);
	playerSprite.setPosition(Vector2f(368.f, 550.f));
	playerHitbox.setSize(Vector2f(100.f, 2.f));
	playerHitbox.setPosition(350.f, 550.f);

	//create display text (I tried creating a function for this but it made it no longer display)
	if (!font.loadFromFile("Assets/font.ttf"))
		std::cout << "Could not load font" << std::endl;

	displayTime.setFont(font);
	displayScore.setFont(font);
	displayLives.setFont(font);

	displayTime.setOutlineThickness(1);
	displayScore.setOutlineThickness(1);
	displayLives.setOutlineThickness(1);

	displayTime.setCharacterSize(16);
	displayScore.setCharacterSize(16);
	displayLives.setCharacterSize(16);

	displayTime.setPosition(Vector2f(0.f, 10.f));
	displayScore.setPosition(Vector2f(0.f, 40.f));
	displayLives.setPosition(Vector2f(0.f, 70.f));

	//create apple collecting sound
	if (!collectBuffer.loadFromFile("Assets/collect.wav"))
		std::cout << "Could not play sound" << std::endl;
	collect.setBuffer(collectBuffer);
	if (!heartBuffer.loadFromFile("Assets/heart.wav"))
		std::cout << "Could not play sound" << std::endl;
	lifeUp.setBuffer(heartBuffer);
	if (!explosionBuffer.loadFromFile("Assets/explosion.wav"))
		std::cout << "Could not play sound" << std::endl;
	explosion.setBuffer(explosionBuffer);
	missedApple.setBuffer(missedAppleBuffer);
	if (!missedAppleBuffer.loadFromFile("Assets/missedApple.wav"))
		std::cout << "Could not play sound" << std::endl;
	missedApple.setBuffer(missedAppleBuffer);
	missedHeart.setBuffer(missedHeartBuffer);
	if (!missedHeartBuffer.loadFromFile("Assets/missedHeart.wav"))
		std::cout << "Could not play sound" << std::endl;
	missedHeart.setBuffer(missedHeartBuffer);

	dt = 0; //deltatime multipier
	multiplier = 60.f; //this multiplier should keep apples around 60fps movement
	appleMultiplier = 1000.f; //this multiplier should keep apples around 60fps movement
	score = 0;
	fallSpeed = .2;
	spawnInterval = 2000;
	lives = 3;
}

Game::~Game() {}

void Game::spawnApple() {
	int chance = rand() % 100 + 1;
	Sprite appleSprite, heartSprite, bombSprite;
	appleSprite.setTextureRect(IntRect(0, 0, 32, 32));
	appleSprite.setPosition((float)(20 + rand() % 750), 0.f);
	heartSprite.setTextureRect(IntRect(0, 0, 32, 32));
	heartSprite.setPosition((float)(20 + rand() % 750), 0.f);
	bombSprite.setTextureRect(IntRect(0, 0, 32, 32));
	bombSprite.setPosition((float)(20 + rand() % 750), 0.f);
	if (chance > 10) {
		appleTexture.loadFromFile("Assets/apple.png");
		if (!appleTexture.loadFromFile("Assets/apple.png"))
			std::cout << "Could not load texture" << std::endl;
		appleSprite.setTexture(appleTexture);
		apples.push_back(std::make_pair(appleSprite, 0));
	}
	if (chance <= 10 && chance > 7) {
		heartTexture.loadFromFile("Assets/heart.png");
		if (!heartTexture.loadFromFile("Assets/heart.png"))
			std::cout << "Could not load texture" << std::endl;
		heartSprite.setTexture(heartTexture);
		apples.push_back(std::make_pair(heartSprite, 1));
	}
	if (chance <= 7) {
		bombTexture.loadFromFile("Assets/bomb.png");
		if (!bombTexture.loadFromFile("Assets/bomb.png"))
			std::cout << "Could not load texture" << std::endl;
		bombSprite.setTexture(bombTexture);
		apples.push_back(std::make_pair(bombSprite, 2));
	}
}