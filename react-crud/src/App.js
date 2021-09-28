import './App.css';
import CRUDTable from './components/CRUDTable';
import CRUD from './components/CRUD';
import Post from './components/Post';
import Top from './components/Top'
import { Navbar, Nav } from 'react-bootstrap';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

function App() {
  return (
    <Router>
      <Navbar bg="light" expand="lg" i>
        <Navbar.Brand href="/">Home</Navbar.Brand>
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="mr-auto">
            <Nav.Link href="/CRUD">Get/Delete</Nav.Link><br></br>
            <Nav.Link href="/CRUDTable">Put</Nav.Link><br></br>
            <Nav.Link href="/Post">Post</Nav.Link><br></br>
            <Nav.Link href="/Top">TopK</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Navbar>
      <Switch>
        <Route path='/CRUDTable' component={CRUDTable} />
        <Route path='/CRUD' component={CRUD} />
        <Route path='/Post' component={Post} />
        <Route path='/Top' component={Top} />
      </Switch>
    </Router>
  );
}

export default App;
