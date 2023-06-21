import random
import sys

HEARTS = chr(9829) # Червы
DIAMONDS = chr(9830) # Буби
SPADES = chr(9824) # Пики
CLUBS = chr(9827) # Трефы
BACKSIDE = 'backside'


def main():
    money = 5000
    while True:
        # Проверяем, не закончились ли деньги:
        if money <= 0:
            print("У тебя не осталось денег! Спасибо за игру!")
            sys.exit()
        # Делаем возможность сделать ставку:
        print(f'Money: {money}')
        bet = get_bet(money)
        # Сдаем дилеру и игроку по две карты из колоды:
        deck = get_deck()
        dealer_hand = [deck.pop(), deck.pop()]
        player_hand = [deck.pop(), deck.pop()]
        # Обработка действий игрока:
        print('Bet:', bet)
        while True:
            display_hands(player_hand, dealer_hand, False)
            print()
            # Проверка на перебор у игрока:
            if get_hand_value(player_hand) > 21:
                break
            # Получаем ход игрока: H, S или D:
            move = get_move(player_hand, money - bet)
            if move == 'D':
                # Игрок удваивает, он может увеличить ставку:
                additional_bet = get_bet(min(bet, (money - bet)))
                bet += additional_bet
                print(f'Ставка повысилась до {bet}')
                print(f'Bet: {bet}')
            if move in ('H', 'D'):
                # Еще и удваиваю: игрок берет еще одну карту.
                new_card = deck.pop()
                rank, suit = new_card
                print(f'Ты вытянул {rank} {suit}')
                player_hand.append(new_card)
                if get_hand_value(player_hand) > 21:
                    continue
            if move in ('S', 'D'):
                # Хватит или удваиваю: переход хода к следующему игроку
                break
        # Обработка действий дилера:
        if get_hand_value(player_hand) <= 21:
            while get_hand_value(dealer_hand) < 17:
                # Дилер берет еще одну карту:
                print('Дилер берет еще одну карту...')
                dealer_hand.append(deck.pop())
                display_hands(player_hand, dealer_hand, False)
                if get_hand_value(dealer_hand) > 21:
                    break
                input('Нажмите Enter для прододжения')
                print('\n\n')
        display_hands(player_hand, dealer_hand, True)
        player_value = get_hand_value(player_hand)
        dealer_value = get_hand_value(dealer_hand)
        # Проверяем, игрок выиграл, проиграл или сыграл вничью:
        if dealer_value > 21:
            print(f'Дилер проиграл! Ты выиграл ${bet}!')
            money += bet
        elif (player_value > 21) or (player_value < dealer_value):
            print(f'Ты проиграл ${bet}!')
            money -= bet
        elif player_value > dealer_value:
            print(f'Ты выиграл ${bet}!')
            money += bet
        elif player_value == dealer_value:
            print(f'У вас ничья, ставка возвращается к тебе.')
        input('Нажмите Enter для продолжения')
        print('\n\n')


def get_bet(max_bet: str) -> int:
    """Спрашиваем у игрока, сколько он ставит на этот раунд."""
    while True:
        print(f'Сколько ты хочешь поставить? 1-{max_bet} or Q(uit)')
        bet = input('> ').upper().strip()
        if bet == "Q":
            print('Спасибо за игру!')
            sys.exit()
        if not bet.isdecimal():
            continue
        bet = int(bet)
        if 1 <= bet <= max_bet:
            return bet


def get_deck() -> list:
    """Возвращаем список кортежей (номинал, масть) для всех 52 карт."""
    deck = []
    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        for rank in range(2, 11):
            deck.append((str(rank), suit))
        for rank in ('J', 'Q', 'K', 'A'):
            deck.append((rank, suit))
    random.shuffle(deck)
    return deck


def display_hands(player_hand: list, dealer_hand: list, show_dealer_hand: bool) -> None:
    """Отображаем карты игрока и дилера. Скоываем первую карту дилера, если show_dealer_hand = False"""
    print()
    if show_dealer_hand:
        print(f'DEALER: {get_hand_value(dealer_hand)}')
        display_cards(dealer_hand)
    else:
        print('DEALER: ???')
        # Скрываем первую карту дилера:
        display_cards([BACKSIDE] + dealer_hand[1:])
    # Отображаем карты игрока:
    print('PLAYER:', get_hand_value(player_hand))
    display_cards(player_hand)


def get_hand_value(cards: list) -> int:
    """Возвращаем стоимость карт"""
    value = 0
    number_of_aces = 0
    # Добавляем стоимость карты - не туза:
    for card in cards:
        rank = card[0]
        if rank == 'A':
            number_of_aces += 1
        elif rank in ('K', 'Q', 'J'):
            value += 10
        else:
            value += int(rank)
    value += number_of_aces
    for i in range(number_of_aces):
        # Если можно добавить еще 10 с перебором, добавляем:
        if value + 10 <= 21:
            value += 10
    return value


def display_cards(cards: list) -> None:
    """Отображаем все карты из списка"""
    rows = ['', '', '', '', '']
    for i, card in enumerate(cards):
        if card == BACKSIDE:
            rows[0] += '|##¯|'
            rows[1] += '|###|'
            rows[2] += '|_##|'
        else:
            rank, suit = card
            rows[0] += '|{}¯¯| '.format(rank.ljust(1))
            rows[1] += '| {} | '.format(suit)
            rows[2] += '|__{}| '.format(rank.rjust(1))
    for row in rows:
        print(row)


def get_move(player_hand: list, money: int) -> str:
    """Спрашиваем, какой ход хочет сделать игрок, возвращаем H, если он хочет взять еще карту,
    S - хватит, D - удваивает"""
    while True:
        moves = ['(H)it', '(S)tand']
        if len(player_hand) == 2 and money > 0:
            moves.append('(D)ouble down')
        move_prompt = ','.join(moves) + '>'
        move = input(move_prompt).upper()
        if move in ('H', 'S'):
            return move
        if move == 'D' and '(D)ouble down' in moves:
            return move


if __name__ == '__main__':
    main()