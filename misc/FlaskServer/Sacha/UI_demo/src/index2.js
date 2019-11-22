import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

var demo = true;

/* hardcode TODO */


function Deck(props) {
    return (
        <button
        className="card_pile"
        onClick={props.onClick}
        >{'Deck: ' + props.value}
        </button>
    )
}

function Card(props) {
    return (
        <button
        className="card"
        onClick={props.onClick}
        >{props.value}
        </button>
    )
}

function Hand(props) {
    return (
        <button
        className="card_hand"
        onClick={props.onClick}
        >{props.value}
        </button>
    )
}

function Arrow(props) {
    return (
        <button
        className="arrow_hand"
        onClick={props.onClick}
        >{props.value}
        </button>
    )
}
  
class Board extends React.Component {
    renderDeck() {
        return (
        <Deck
        value={this.props.deck}
        onClick={() => this.props.deckClick()}
        />
        );
    }

    renderCard() {
        return (
        <Card
        value={null}
        onClick={() => this.props.cardClick()}
        />
        );
    }

    renderHand() {
        return (
        <Hand
        value={null}
        onClick={() => this.props.cardClick()}
        />
        );
    }

    renderArrow(char) {
        return (
        <Arrow
        value={char}
        onClick={() => this.props.cardClick()}
        />
        );
    }
  
    render() {
        return (
        <div>
            <div className="card-row">
                {this.renderArrow('<-')}
                {this.renderHand(0)}
                {this.renderHand(1)}
                {this.renderHand(2)}
                {this.renderHand(3)}
                {this.renderHand(4)}
                {this.renderHand(5)}
                {this.renderArrow('->')}
            </div>
            <div className="card-row">
                {this.renderDeck()}
                {this.renderCard(0)}
                {this.renderCard(1)}
                {this.renderCard(2)}
                {this.renderCard(3)}
                {this.renderDeck()}
            </div>
            <div className="card-row">
                {this.renderDeck()}
                {this.renderCard(0)}
                {this.renderCard(1)}
                {this.renderCard(2)}
                {this.renderCard(3)}
                {this.renderDeck()}
            </div>
            <div className="card-row">
                {this.renderArrow('<-')}
                {this.renderHand(0)}
                {this.renderHand(1)}
                {this.renderHand(2)}
                {this.renderHand(3)}
                {this.renderHand(4)}
                {this.renderHand(5)}                
                {this.renderArrow('->')}
            </div>
        </div>
        );
    }
}
  
class Game extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            deck1: Array(30).fill(null),
            field1: Array(4).fill(null),
            grave1: Array(30).fill(null),
            hand1: Array(30).fill(null),
            ds1: 0,
            gs1: 0,
            hs1: 0,
            deck2: Array(30).fill(null),
            field2: Array(4).fill(null),
            grave2: Array(30).fill(null),
            hand2: Array(30).fill(null),
            ds2: 0,
            gs2: 0,
            hs2: 0,
            stepNumber: 0,
            oneIsNext: true,
            mana1: 30,
            mana2: 30,
        };
    }

    jumpTo(step) {
        this.setState({
            stepNumber: step,
            xIsNext: (step % 2) === 0,
        });
    }

    handleClick(i) {
        const history = this.state.history.slice(0,
            this.state.stepNumber + 1);
        const current = history[history.length - 1];
        const squares = current.squares.slice();
        if (squares[i]) {
            return;
        }
        squares[i] = this.state.xIsNext ? 'X' : 'O';
        this.setState({
            history: history.concat([{
                squares: squares,
            }]),
            stepNumber: history.length,
            xIsNext: !this.state.xIsNext,
        });
    }

    handleCardButton(card) {
        return null
    }

    render() {
        const deck_back = this.state.deck1.length;
        const field1 = this.state.field1.map((card, pos) =>
        this.handleCardButton(card)
        );


        return (
        <div className="game">
            <div className="game-board">
                <Board
                deckClick={() => this.handleDraw()}
                onClick={(i) => this.handleClick(i)}
                />
            </div>
            
        </div>
        );
    }
}

/*
<div className="game-info">
    <div>{status}</div>
    <ol>{moves}</ol>
</div>
*/
  
// ========================================
  
ReactDOM.render(
    <Game player={0}/>,
    document.getElementById('root')
);