#include "MainMenu.h"
#include "game.h"

MainMenu::MainMenu(float width, float height) {
	
	if (!font.loadFromFile("Assets/font.ttf")) {
		std::cout << "Could not load font " << std::endl;
	}

	mainMenu[0].setFont(font);
	mainMenu[0].setFillColor(Color::Red);
	mainMenu[0].setString("Play");
	mainMenu[0].setCharacterSize(64);
	mainMenu[0].setOutlineThickness(2);
	mainMenu[0].setPosition(300, 200);

	mainMenu[1].setFont(font);
	mainMenu[1].setString("Credits");
	mainMenu[1].setCharacterSize(64);
	mainMenu[1].setOutlineThickness(2);
	mainMenu[1].setPosition(200, 300);

	mainMenu[2].setFont(font);
	mainMenu[2].setString("Exit");
	mainMenu[2].setCharacterSize(64);
	mainMenu[2].setOutlineThickness(2);
	mainMenu[2].setPosition(300, 400);

	MainMenuSelected = 0;

}
MainMenu::~MainMenu() {}

void MainMenu::draw(RenderWindow& window) {
	for (int i = 0; i < Max_main_menu; i++) {
		window.draw(mainMenu[i]);
	}
}

void MainMenu::MoveUp() {
	if (MainMenuSelected - 1 >= 0) {
		mainMenu[MainMenuSelected].setFillColor(Color::White);

		MainMenuSelected--;
		if (MainMenuSelected == -1) 
			MainMenuSelected = 2;
		mainMenu[MainMenuSelected].setFillColor(Color::Red);
	}
}

void MainMenu::MoveDown() {
	if (MainMenuSelected + 1 <= Max_main_menu) {
		mainMenu[MainMenuSelected].setFillColor(Color::White);

		MainMenuSelected++;
		if (MainMenuSelected == 3) 
			MainMenuSelected = 0;

		mainMenu[MainMenuSelected].setFillColor(Color::Red);
	}
}