# Custom Hooks

### App.css
```css
#root {
  margin: 0 auto;
}

#root button {
  margin: 4px;
  background-color: #f0f0f0;
}
```

### useCounter.js
```js
import { useState } from 'react'

function useCounter(initialValue = 0) {
  const [count, setCount] = useState(initialValue)

  const increment = () => {
    setCount((prev) => prev + 1)
  }

  const decrement = () => {
    setCount((prev) => prev - 1)
  }

  return { count, increment, decrement }
}

export default useCounter
```

### App.jsx
```js
import './App.css'
import useCounter from './hooks/useCounter'

const App = () => {
  const { 
    count, increment, decrement 
  } = useCounter(0)

  return (
    <>
      <h2>Counter: {count}</h2>
      <button onClick={increment}>
        Increment
      </button>
      <button onClick={decrement}>
        Decrement
      </button>
    </>
  )
}

export default App
```

<hr/>

### useWindowSize.js
```js
import { useState, useEffect } from 'react'

function useWindowSize() {
  const [windowSize, setWindowSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight
  })

  useEffect(() => {
    const handleResize = () => {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight
      })
    }
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener(
      'resize', handleResize)
  }, [])

  return windowSize
}

export default useWindowSize
```


### App.jsx
```js
import './App.css'
import useWindowSize
 from './hooks/useWindowSize'

const App = () => {
  const {width, height}
   = useWindowSize()

  return (
    <>
      <h2>Window Size</h2>
      <p>Width: {width}</p>
      <p>Height: {height}</p>
    </>
  )
}

export default App
```

## Server
### package.json
```json
{
  "name": "book-server",
  "version": "1.0.0",
  "main": "index.js",
  "scripts": {
    "start": "node index.js"
  },
  "dependencies": {
    "cors": "^2.8.5",
    "express": "^4.18.2"
  }
}
```

### index.js
```js
const express = require('express')
const cors = require('cors')
const app = express()

app.use(cors())

const PORT = 3000

const books = [
  { 
    id: 1, 
    title: 'The Great Gatsby', 
    author: 'Scott Fitzgerald' 
  }, { 
    id: 2,
    title: '1984',
    author: 'George Orwell'
  }, { 
    id: 3,
    title: "Hamlet",
    author: "Shakespeare" 
  }
]

app.get('/books', (req, res) => {
  setTimeout(() => {
    res.json(books)
  }, 1000)
})

app.get('/wrong', (req, res) => {
  setTimeout(() => {
    res.status(500).json({ 
      error: 'Error' 
    })
  }, 1000)
})

app.listen(PORT, () => {
  console.log(
    `On http://localhost:${PORT}`)
})
```

## Client
### useFetch.js
```js
import { useState, useEffect } from 'react'

export const useFetch = (url) => {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(url)
        if (!response.ok) {
          throw new Error('Error')
        }
        const result = await response.json()
        setData(result)
      } catch (err) { setError(err.message)
      } finally { setLoading(false) }
    }
    fetchData()
  }, [])

  return { data, loading, error }
}
```


### App.jsx
```js
import './App.css'
import { useFetch } from './hooks/useFetch'

const App = () => {
  const { data, loading, error }
   = useFetch('http://localhost:3000/books')

  return (
    <>
      <h2>Book List</h2>
      {loading ? <p>Loading...</p>
      : error ? <p>Error: {error}</p> 
      : (
      <ul>
        {data.map(book => (
        <li key={book.id}>
          <strong>{book.title} </strong>
          by {book.author}
        </li>))}
      </ul>)}
    </>
  )
}
export default App
```
