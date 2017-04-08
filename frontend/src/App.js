import React, { Component } from 'react';
import './App.css';
import '../semantic/dist/semantic.min.css'

class App extends Component {
  render() {
    return (
      <div className="ui fluid container">
        <h2 className="ui center aligned header pg-header">
          <i className="write square icon"></i>
          Ancient Chinese Poem Generator
        </h2>
        <div className="ui icon input">
          <input className="pg-input" placeholder="type a keyword"/>
          <i className="send outline link icon"></i>
        </div>
        <ul className="pg-output">
          <li>珠帘高捲莫轻遮，</li>
          <li>往往相逢隔岁华，</li>
          <li>春气昨宵飘律管，</li>
          <li>东风今日放梅花。</li>
        </ul>
      </div>
    );
  }
}

export default App;
