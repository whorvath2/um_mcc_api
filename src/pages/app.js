import {useState} from 'react';
import {BrowserRouter as Router} from 'react-router-dom';
import './App.css';
import Search from './search';
import Announcer from './announcer';

function findStaff(query) {
    if (!query) {
        return []
    }
    return fetch(`http://localhost:8662/um_mcc/find?${query}`)
        .then(response => response.json())
        .then(json => JSON.parse(json))
        .catch(error => console.log(error))
}

const App = () => {
    const search = window.location.search;
    const query = new URLSearchParams(search);
    const [searchQuery, setSearchQuery] = useState(query || '');
    const staff = findStaff(searchQuery);

    return (
        <Router>
            <div className="App">
                <Announcer
                    message={`${staff.length} staff found`}
                />
                <Search
                    searchQuery={searchQuery}
                    setSearchQuery={setSearchQuery}
                />
                <ul>
                    {
                        staff.map((staffer) => (
                            <li key={staffer}>{staffer.name} {staffer.title} {staffer.department} {staffer.salary}</li>
                        ))
                    }
                </ul>
            </div>
        </Router>
    );
};

export default App;