'use strict';

/* component start */

class Welcome extends React.Component {
  render() {
    return React.createElement(
      'p',
      null,
      ' Welcome to DanceDestination!'
    );
  }
}
/* component end */

/* render start */
ReactDOM.render(React.createElement(Welcome, null), document.getElementById('welcome'));
/* render end */

/* component start */
class Images extends React.Component {
  render() {
    return React.createElement(
      React.Fragment,
      null,
      React.createElement('img', { src: 'static/img/dance_1.jpg' }),
      React.createElement('img', { src: 'static/img/dance_2.jpg' }),
      React.createElement('img', { src: 'static/img/dance_3.jpg' }),
      React.createElement('img', { src: 'static/img/dance_4.jpg' })
    );
  }
}

/* component end */

/* render start */
ReactDOM.render(React.createElement(Images, null), document.getElementById('header-image'));
/* render end */

/* component start */
class Title extends React.Component {
  render() {
    return React.createElement(
      React.Fragment,
      null,
      React.createElement(
        'h4',
        null,
        'What Are You in the Mood for Today?'
      )
    );
  }
}

/* component end */

/* render start */
ReactDOM.render(React.createElement(Title, null), document.getElementById('title'));
/* render end */

/* component start */
class FooterImages extends React.Component {
  render() {
    return React.createElement(
      React.Fragment,
      null,
      React.createElement('img', { src: 'static/img/dance_5.jpg' }),
      React.createElement('img', { src: 'static/img/dance_6.jpg' }),
      React.createElement('img', { src: 'static/img/dance_7.jpg' }),
      React.createElement('img', { src: 'static/img/dance_8.jpg' })
    );
  }
}

/* component end */

/* render start */
ReactDOM.render(React.createElement(FooterImages, null), document.getElementById('footer-image'));
/* render end */

