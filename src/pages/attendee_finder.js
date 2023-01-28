'use strict';

const e = React.createElement;

class Attendees extends React.Component {
  constructor(props) {
    super(props);
    this.state = { attendees: [] };
  }

  render() {
    if (this.state.attendees.length > 0) {
      return this.state.attendees.join(", ")
    }
    return e(
        'button',
        { onClick: () => this.setState({ attendees:  ["Bill", "Jon"]})},
        'Add Attendee'
    );
  }
}

const domContainer = document.querySelector('#attendee_finder');
const root = ReactDOM.createRoot(domContainer);
root.render(e(Attendees));