# Lifecycle and useEffect

### App.css
```css
#root {
  margin: 0 auto;
}

#root button {
  margin: 4px;
  background-color: #f0f0f0;
}

label {
  font-size: 1.2em;
  margin-right: 0.6em;
  cursor: pointer;
}
```

### ClassComp.jsx
```js
import { Component } from 'react'

class ClassComp extends Component {
  constructor(props) {
    super(props)
    this.state = { count: 0 }
  }

  componentDidMount() {
    console.log('1. Mounted')
  }

  componentDidUpdate() {
    console.log('2. Updated')
  }

  componentWillUnmount() {
    console.log('3. Unmounted')
  }

  handleIncrement = () => {
    this.setState(prevState => (
      { count: prevState.count + 1 }
    ))
  }

  render() {
    console.log('-- Rendering --')
    return (
      <div>
        <h2>Class Component</h2>
        <h3>Count: {this.state.count}</h3>
        <button onClick={this.handleIncrement}>
          Increase
        </button>
      </div>
    )
  }
}

export default ClassComp
```

### FuncComp.jsx
```js
import { useState, useEffect } from 'react'

const FuncComp = () => {
  const [count, setCount] = useState(0)

  useEffect(() => {
    console.log('1. Mounted')
    return () => {
      console.log('3. Unmounted')
    }
  }, [])

  useEffect(() => {
    console.log('1. Mounted / 3. Updated')
  }, [count])

  const handleIncrement = () => {
    setCount(prevCount => prevCount + 1)
  }

  console.log('-- Rendering --')

  return (
    <div>
      <h2>Function Component</h2>
      <h3>Count: {count}</h3>
      <button onClick={handleIncrement}>
        Increase
      </button>
    </div>
  )
}

export default FuncComp
```

### App.jsx
```js
import './App.css'
import ClassComp from './ClassComp'
import FuncComp from './FuncComp'
import { useState } from 'react'

const App = () => {
  const [selected, setSelected] = useState('')

  return (
    <>
      {['', 'ClassComp', 'FuncComp'].map((option) => (
        <label key={option}>
          <input
            type="radio" value={option}
            checked={selected === option}
            onChange={(e) => setSelected(e.target.value)}/>
          {option || 'None'}
        </label>
      ))}
      {selected && (selected === 'ClassComp' ? <ClassComp /> : <FuncComp />)}
    </>
  )
}
export default App
```

<hr/>

### App.jsx
```js
import './App.css'
import { useState, useEffect } from 'react'

const App = () => {
  const [count1, setCount1] = useState(0)
  const [count2, setCount2] = useState(0)

  const handleIncrease = (setter) => { setter((prev) => prev + 1) }

  useEffect(() => {
    console.log(`C1: ${count1}, C2: ${count2}`)
  }, [count1])

  return (
    <div>
      <h2>Count1: {count1}</h2>
      <button onClick={() => handleIncrease(setCount1)}>Count1++</button>

      <h2>Count2: {count2}</h2>
      <button onClick={() => handleIncrease(setCount2)}>Count2++</button>
    </div>
  )
}

export default App
```

<hr/>

### public/data/books.json
```json
[
  {
    "id": 1,
    "title": "React Basics",
    "author": "John Doe"
  },
  {
    "id": 2,
    "title": "Advanced React",
    "author": "Jane Smith"
  },
  {
    "id": 3,
    "title": "JavaScript Essentials",
    "author": "Alan Turing"
  },
  {
    "id": 4,
    "title": "CSS Mastery",
    "author": "Rachel Green"
  }
]
```

### App.jsx
```js
import './App.css'
import { useState, useEffect } from 'react'

const App = () => {
  const [books, setBooks] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchBooks = async () => {
      try {
        const response = await fetch('/data/books.json')
        const data = await response.json()
        setBooks(data)
      } catch (error) {
        console.error('Failed to fetch books:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchBooks()
  }, [])

  if (loading) return <p>Loading...</p>

  return (
    <div>
      <h2>Book List</h2>
      <ul>
        {books.map((book) => (
          <li key={book.id}>
            <strong>{book.title}</strong> by {book.author}
          </li>
        ))}
      </ul>
    </div>
  )
}

export default App
```

<hr/>

### Timer.jsx
```js
import { useState, useEffect } from 'react'

const Timer = () => {
  const [seconds, setSeconds] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => {
      setSeconds((prev) => prev + 1)
    }, 1000)

    return () => {
      clearInterval(interval)
      console.log('Timer cleaned up')
    }
  }, [])

  return <p>Timer: {seconds} seconds</p>
}

export default Timer
```

### App.jsx
```js
import './App.css'
import { useState } from 'react'
import Timer from './Timer'

const App = () => {
  const [showTimer, setShowTimer]
   = useState(false)

  return (
    <>
      <label>
        <input
          type="checkbox"
          checked={showTimer}
          onChange={
            (e) => setShowTimer(
              e.target.checked
            )}/>
        Show Timer
      </label>
      {showTimer && <Timer />}
    </>
  )
}

export default App
```
