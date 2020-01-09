'use strict';

/* component start */ 
class Welcome extends React.Component {
  render() {
    return <p> Welcome to DanceDestination!</p>;
  }
}
/* component end */


/* render start */
ReactDOM.render(
  <Welcome />,
  document.getElementById('welcome')
);
/* render end */



/* component start */ 
class Images extends React.Component {
    render() {
      return (
        <React.Fragment>
            <img src='static/img/dance_1.jpg'/>
            <img src='static/img/dance_2.jpg'/>
            <img src='static/img/dance_3.jpg'/>
            <img src='static/img/dance_4.jpg'/>
        </React.Fragment>
      );
    }
}

/* component end */


/* render start */
ReactDOM.render(
  <Images />,
  document.getElementById('header-image')
);
/* render end */



/* component start */ 
class Title extends React.Component {
    render() {
      return (
        <React.Fragment>
            <h4>What Are You in the Mood for Today?</h4>
        </React.Fragment>
      );
    }
}

/* component end */


/* render start */
ReactDOM.render(
  <Title />,
  document.getElementById('title')
);
/* render end */


/* component start */ 
class FooterImages extends React.Component {
    render() {
      return (
        <React.Fragment>
            <img src='static/img/dance_5.jpg'/>
            <img src='static/img/dance_6.jpg'/>
            <img src='static/img/dance_7.jpg'/>
            <img src='static/img/dance_8.jpg'/>
        </React.Fragment>
      );
    }
}

/* component end */


/* render start */
ReactDOM.render(
  <FooterImages />,
  document.getElementById('footer-image')
);
/* render end */



 