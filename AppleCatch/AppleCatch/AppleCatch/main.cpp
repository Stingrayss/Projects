#include "game.h"
#include "MainMenu.h"
#include <SFML/Audio.hpp>

//create menus and then I think that's a good place to call it

int main()
{
	RenderWindow menu(VideoMode(800, 600), "AppleCatch", Style::Default);
	MainMenu mainMenu(menu.getSize().x, menu.getSize().y);

	Font font;
	if (!font.loadFromFile("Assets/font.ttf"))
		std::cout << "Could not load font" << std::endl;

	//make mainmenu score display
	Text score, timer;
	score.setFont(font);
	score.setCharacterSize(16);
	score.setOutlineThickness(1);
	score.setPosition(10, 580);
	score.setString("Previous Attempt's Score: 0");
	timer.setFont(font);
	timer.setCharacterSize(16);
	timer.setOutlineThickness(1);
	timer.setPosition(10, 560);
	timer.setString("Previous Attempt's Time: 0");

	//create menu background
	Texture menuTexture;
	menuTexture.loadFromFile("Assets/background.png", IntRect(0, 0, 800, 600));
	if (!menuTexture.loadFromFile("Assets/background.png"))
		std::cout << "Could not load texture" << std::endl;
	Sprite menuBackground;
	menuBackground.setTexture(menuTexture);

	while (menu.isOpen())
	{
		Event event;

		while (menu.pollEvent(event))
		{
			if (event.type == Event::Closed)
				menu.close();

			if (event.type == Event::KeyReleased) {
				if (event.key.code == Keyboard::Up or event.key.code == Keyboard::W) {
					mainMenu.MoveUp();
					break;
				}

				if (event.key.code == Keyboard::Down or event.key.code == Keyboard::S) {
					mainMenu.MoveDown();
					break;
				}
				if (event.key.code == Keyboard::Return or event.key.code == Keyboard::Space) {
					RenderWindow window(VideoMode(800, 600), "AppleCatch", Style::Default);
					RenderWindow Credits(VideoMode(800, 600), "AppleCatch");

					int x = mainMenu.MainMenuPressed();
					//play game
					if (x == 0) {
						Credits.close();

						//initiate music (has to be done outside of the game class because it's not loading, it's opening
						//at least I think, putting it in the class caused the game to run without displaying anything and causing lives to be lost
						Music music;
						if (!music.openFromFile("Assets/music.wav"))
							std::cout << "Could not play music" << std::endl;
						music.play();
						music.setVolume(15);
						music.setLoop(true);

						Game game;

						while (window.isOpen())
						{
							Event event;

							std::string time = std::to_string(game.gameTime.getElapsedTime().asSeconds());
							time.erase(time.begin() + 5, time.end());

							while (window.pollEvent(event))
							{
								if (event.type == Event::Closed) {
									window.close();
									score.setString("Previous Attempt's Score: " + std::to_string(game.score));
									timer.setString("Previous Attempt's Score: " + time);
								}
								if (event.type == Event::KeyPressed) {
									if (event.key.code == Keyboard::Escape)
										window.close();
								}
							}
							//delta time multiplier
							game.dt = game.clock.restart().asSeconds();

							//set the display text
							game.displayTime.setString("Timer: " + time);
							game.displayScore.setString("Score: " + std::to_string(game.score));
							game.displayLives.setString("Lives: " + std::to_string(game.lives));

							//movement control
							//has some super basic wrapping and many different keybinds to move with
							if (Keyboard::isKeyPressed(Keyboard::A) or Keyboard::isKeyPressed(Keyboard::G) or Keyboard::isKeyPressed(Keyboard::Left)) {
								if ((int)game.playerHitbox.getPosition().x + 100 == 0) {
									game.playerHitbox.setPosition(790.f, game.playerHitbox.getPosition().y);
									game.playerSprite.setPosition(808.f, game.playerHitbox.getPosition().y);
								}
								if (Keyboard::isKeyPressed(Keyboard::LShift) or Keyboard::isKeyPressed(Keyboard::RShift)) {
									game.playerHitbox.move(-20.f * game.dt * game.multiplier, 0.f);
									game.playerSprite.move(-20.f * game.dt * game.multiplier, 0.f);
								}

								game.playerHitbox.move(-5.f * game.dt * game.multiplier, 0.f);
								game.playerSprite.move(-5.f * game.dt * game.multiplier, 0.f);
							}
							if (Keyboard::isKeyPressed(Keyboard::D) or Keyboard::isKeyPressed(Keyboard::K) or Keyboard::isKeyPressed(Keyboard::Right)) {
								if ((int)game.playerHitbox.getPosition().x - 20 == 800) {
									game.playerHitbox.setPosition(-100.f, game.playerHitbox.getPosition().y);
									game.playerSprite.setPosition(-83.f, game.playerHitbox.getPosition().y);
								}
								if (Keyboard::isKeyPressed(Keyboard::LShift) or Keyboard::isKeyPressed(Keyboard::RShift)) {
									game.playerHitbox.move(20.f * game.dt * game.multiplier, 0.f);
									game.playerSprite.move(20.f * game.dt * game.multiplier, 0.f);
								}

								game.playerHitbox.move(5.f * game.dt * game.multiplier, 0.f);
								game.playerSprite.move(5.f * game.dt * game.multiplier, 0.f);
							}

							//spawn an apple (starts at 2 seconds, max speed is .5 seconds)
							if (game.appleClock.getElapsedTime().asMilliseconds() >= game.spawnInterval) {
								game.spawnApple();
								game.appleClock.restart();
							}

							//draw to the screen
							window.clear();
							window.draw(game.backgroundSprite);
							window.draw(game.playerHitbox);
							window.draw(game.playerSprite);
							window.draw(game.displayTime);
							window.draw(game.displayScore);
							window.draw(game.displayLives);

							//draw apples
							for (const std::pair<Sprite, int>& pair : game.apples)
								window.draw(pair.first);

							//apple movement
							for (size_t i = 0; i < game.apples.size(); i++) {
								game.apples[i].first.move(Vector2f(0.f, game.fallSpeed * game.dt * game.appleMultiplier));
								if (game.apples[i].first.getPosition().y + 20 >= 540 && game.apples[i].first.getPosition().y + 20 <= 560) {
									if (game.apples[i].first.getPosition().x > game.playerHitbox.getPosition().x - 20 &&
										game.apples[i].first.getPosition().x < game.playerHitbox.getPosition().x + 100) {
										if (game.apples[i].second == 0) {
											game.collect.play();
											game.apples.erase(game.apples.begin() + i);
											if (!(game.spawnInterval <= 500))
												game.spawnInterval -= 25;
											if (!(game.fallSpeed >= 1.00))
												game.fallSpeed += .01;
											game.score += 1;
											break; //VERY IMPORTANT, WILL CAUSE CRASHING WITHOUT THIS
										}
										if (game.apples[i].second == 1) {
											game.lifeUp.play();
											game.apples.erase(game.apples.begin() + i);
											game.lives += 1;
											break; //VERY IMPORTANT, WILL CAUSE CRASHING WITHOUT THIS
										}
										if (game.apples[i].second == 2) {
											game.explosion.play();
											game.apples.erase(game.apples.begin() + i);
											game.lives -= 1;
											break; //VERY IMPORTANT, WILL CAUSE CRASHING WITHOUT THIS
										}
									}
								}
								if (game.apples[i].first.getPosition().y > 600) {
									if (game.apples[i].second == 0) {
										game.lives--;
										game.missedApple.play();
									}
									if (game.apples[i].second == 1) {
										game.missedHeart.play();
									}
									if (game.lives <= 0) {
										window.close();
										score.setString("Previous Attempt's Score: " + std::to_string(game.score));
										timer.setString("Previous Attempt's Score: " + time);
									}
									game.apples.erase(game.apples.begin() + i);
								}

							}
							window.display();
						}
					}

					//credits menu
					if (x == 1) {
						window.close();
						while (Credits.isOpen()) {
							Event aevent;
							while (Credits.pollEvent(aevent))
							{
								if (aevent.type == Event::Closed)
									Credits.close();
								if (aevent.type == Event::KeyPressed) {
									if (aevent.key.code == Keyboard::Escape)
										Credits.close();
								}
							}
							Text creditsText;
							creditsText.setFont(font);
							creditsText.setString("Final IS50B Project \n\n\n      Made by: \n\n    Cade Duncan \n\n\n Thank You Kerney!");
							creditsText.setCharacterSize(32);
							creditsText.setOutlineThickness(2);
							creditsText.setPosition(100, 200);

							Credits.draw(menuBackground);
							Credits.draw(creditsText);
							Credits.display();
						}
					}
					//exit menu
					if (x == 2)
						menu.close();
					break;
				}
			}
		}
		//draw menu
		menu.clear();
		menu.draw(menuBackground);
		menu.draw(score);
		menu.draw(timer);
		mainMenu.draw(menu);
		menu.display();
	}
	return 0;
}