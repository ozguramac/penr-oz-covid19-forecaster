'use strict';

const e = React.createElement;

class ForecastComponent extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return e(
            'div',
            {className: 'container'},
            '...'
        );
    }
}

const domContainer = document.querySelector('#forecast-container');
ReactDOM.render(e(ForecastComponent), domContainer);