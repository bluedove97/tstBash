# Routing

<code>App.css</code>
```css
#root {
  margin: 0 auto;
}

#root button {
  margin: 4px;
  background-color: #f0f0f0;
}

#root nav > * {
  margin: 0 6px;
}
```

<code>Home.jsx</code>
```js
const Home = () => (
  <>
    <h2>Home</h2>
    <p>
      Welcome to Web Dev Class!
    </p>
  </>
)

export default Home
```

<code>About.jsx</code>
```js
const About = () => (
  <>
    <h2>About</h2>
    <ul>
      {['HTML', 'CSS', 'JavaScript']
        .map((item, idx) => (
          <li key={idx}>{item}</li>
        )
      )}
    </ul>
  </>
)

export default About
```

<code>Contact.jsx</code>
```js
const Contact = () => (
  <>
    <h2>Contact</h2>
    <address>
      email: 
      <a href="mailto:yalco@yalco.kr">
          yalco@yalco.kr
      </a>
    </address>
  </>
)

export default Contact
```


<code>App.jsx</code>
```js
import './App.css'
import { BrowserRouter, Routes, Route, Link }
 from 'react-router-dom'

import Home from './pages/Home'
import About from './pages/About'
import Contact from './pages/Contact'

function App() {
  return (
    <BrowserRouter>
      <nav>
        <Link to={'/'}>Home</Link>
        <Link to={'/about'}>About</Link>
        <Link to={'/contact'}>Contact</Link>
      </nav>
      <Routes>
        <Route path='/'
         element={<Home />} />
        <Route path='/about'
         element={<About />} />
        <Route path='/contact'
         element={<Contact />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
```

<hr/>

<code>App.jsx</code>
```js
import { Routes, Route, useNavigate }
 from 'react-router-dom'

import Home from './pages/Home'
import About from './pages/About'
import Contact from './pages/Contact'

function App() {
  const navigate = useNavigate()

  const navTo = (path) => {
    navigate(path)
  }

  return (
    <>
      <button onClick={() => navTo('/')}>
        Home
      </button>
      <button onClick={() => navTo('/about')}>
        About
      </button>
      <button onClick={() => navTo('/contact')}>
        Contact
      </button>
      <Routes>
        <Route path='/'
         element={<Home />} />
        <Route path='/about'
         element={<About />} />
        <Route path='/contact'
         element={<Contact />} />
      </Routes>
    </>
  )
}

export default App
```


<hr/>

<code>App.jsx</code>
```js
import './App.css'
import { Routes, Route, useParams, useLocation }
 from 'react-router-dom'
import React, { useEffect } from 'react'

function Home() {
  const location = useLocation()

  useEffect(() => {
    console.log('Current Path:', location.pathname)
  }, [location])

  return <h1>Home Page</h1>
}

function User() {
  const { id } = useParams()
  const location = useLocation()

  useEffect(() => {
    console.log('Current Path:', location.pathname)
    console.log('URL Parameter (id):', id)
  }, [id, location])

  return <h1>User ID: {id}</h1>
}

function Search() {
  const location = useLocation()
  const queryParams
   = new URLSearchParams(location.search)
  const keyword = queryParams.get('keyword')

  useEffect(() => {
    console.log('Current Path:', location.pathname)
    console.log(
      'Query Parameter (keyword):', keyword
    )}, [keyword, location])

  return <h1>Search Keyword: {keyword}</h1>
}

function App() {
  return (
    <Routes>
      <Route path='/' element={<Home />} />
      <Route path='/user/:id' element={<User />} />
      <Route path='/search' element={<Search />} />
    </Routes>
  )
}

export default App
```

<hr/>

<code>App.jsx</code>
```js
import './App.css'
import { Routes, Route, Link } from 'react-router-dom'

const App = () => {
  return (
    <>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/about">About</Link>
        <Link to="/wrong-path">Wrong Path</Link>
      </nav>
      <Routes>
        <Route path="/" element={<h2>Home Page</h2>} />
        <Route path="/about" element={<h2>About Page</h2>} />
        <Route path="*" element={<h2>404 - Page Not Found</h2>} />
      </Routes>
    </>
  )
}

export default App
```
