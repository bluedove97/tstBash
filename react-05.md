# useReducer

### App.css
```css
#root {
  margin: 0 auto;
}

#root button {
  margin: 4px;
  padding: 0.4em 0.8em;
  background-color: #f0f0f0;
}

input[type=text] {
  display: block;
  margin: 8px 0;
  padding: 4px;
  font-size: 0.92em;
}
```

### App.jsx
```js
import './App.css'
import { useState } from 'react'

function App() {
  const [name, setName] = useState('')
  const [year, setYear] = useState('')
  const [warning, setWarning] = useState('')

  const handleNameChange = (newName) => {
    const formattedName
     = newName.trim().toLowerCase()
    setName(formattedName)
  }

  const handleYearChange = (newYear) => {
    const age = new Date().getFullYear() - newYear
    if (age < 18) {
      setWarning('Must be at least 18 yrs old!')
    } else {
      setWarning('')
      setYear(newYear)
    }
  }

  return (
    <div>
      <input
        type="text"
        placeholder="Enter name"
        value={name}
        onChange={
          (e) => handleNameChange(e.target.value)}
      />
      <input
        type="number"
        placeholder="Enter birth year"
        value={year}
        onChange={
          (e) => handleYearChange(e.target.value)}
      />
      {
        warning && (
          <p style={{ color: 'red' }}>{warning}</p>
        )
      }
      <p>Name: {name}</p>
      <p>Year: {year}</p>
    </div>
  )
}

export default App
```

<hr/>

### reducers/userReducer.js
```js
export const initialState = {
  name: '',
  year: '',
  warning: ''
}

export function userReducer(state, action) {
  switch (action.type) {
    case 'SET_NAME':
      return { 
        ...state, 
        name: action.payload.trim().toLowerCase() }
    case 'SET_YEAR':
      const age
       = new Date().getFullYear() - action.payload
      if (age < 18) {
        return { 
          ...state, 
          warning: 'Must be at least 18 yrs old!' }
      }
      return { 
        ...state, 
        year: action.payload, 
        warning: '' }
    default:
      throw new Error('Unknown action type')
  }
}
```

### App.jsx
```js
import './App.css'
import React, { useReducer } from 'react'
import { userReducer, initialState }
 from './reducers/userReducer'

function App() {
  const [state, dispatch]
   = useReducer(userReducer, initialState)

  return (
    <div>
      <input
        type="text" placeholder="Enter name"
        value={state.name}
        onChange={(e) => dispatch({ 
          type: 'SET_NAME',  payload: e.target.value })}
      />
      <input
        type="number" placeholder="Enter birth year"
        value={state.year}
        onChange={(e) => dispatch({ 
          type: 'SET_YEAR', payload: e.target.value })}
      />
      {state.warning
       && <p style={{ color: 'red' }}>{state.warning}</p>}
      <p>Name: {state.name}</p>
      <p>Year: {state.year}</p>
    </div>
  )
}

export default App
```

<hr/>

### data.js
```js
const externalData = {
  name: 'jane doe',
  year: 1995
}

export default externalData
```

### reducers/userReducer.js
```js
export const initialState = {
  name: '',
  year: '',
  warning: ''
}

export function userReducer(state, action) {
  switch (action.type) {
    case 'SET_NAME':
      return { 
        ...state, 
        name: action.payload.trim().toLowerCase() }
    case 'SET_YEAR':
      const age
       = new Date().getFullYear() - action.payload
      if (age < 18) {
        return { 
          ...state, 
          warning: 'Must be at least 18 yrs old!' }
      }
      return { 
        ...state, 
        year: action.payload, 
        warning: '' }
    case 'RESET':
      return init(action.payload)
    default:
      throw new Error('Unknown action type')
  }
}

export function init(externalData) {
  return {
    ...initialState,
    name: externalData.name,
    year: externalData.year
  }
}
```

### App.jsx
```js
import './App.css'
import React, { useReducer } from 'react'
import { userReducer, init }
 from './reducers/userReducer'
import data from './data'

function App() {
  const [state, dispatch]
   = useReducer(userReducer, data, init)

  return (
    <div>
      <input
        type="text" placeholder="Enter name"
        value={state.name}
        onChange={(e) => dispatch({ 
          type: 'SET_NAME',  payload: e.target.value })}
      />
      <input
        type="number" placeholder="Enter birth year"
        value={state.year}
        onChange={(e) => dispatch({ 
          type: 'SET_YEAR', payload: e.target.value })}
      />
      {state.warning
       && <p style={{ color: 'red' }}>{state.warning}</p>}
      <p>Name: {state.name}</p>
      <p>Year: {state.year}</p>
      <button onClick={
        () => dispatch({ type: 'RESET', payload: data })}>
        Reset
      </button>
    </div>
  )
}

export default App
```

<hr/>

### reducers/countReducer.js
```js
export const initialState = {
  count: 0
}

export function countReducer(state, action) {
  const { value } = action.payload
  const { x, y } = action.meta
  switch (action.type) {
    case 'INC':
      console.log(`Click: (${x}, ${y})`)
      return { 
        ...state, 
        count: state.count + value
      }
    case 'DEC':
      console.log(`Click: (${x}, ${y})`)
      return { 
        ...state,
        count: state.count - value 
      }
    default:
      throw new Error('Unknown action type')
  }
}
```

### App.jsx
```js
import './App.css'
import React, { useReducer } from 'react'
import { countReducer, initialState }
 from './reducers/countReducer'

function App() {
  const [state, dispatch]
   = useReducer(countReducer, initialState)

  const handleClick = (type, value, event) => {
    const { clientX: x, clientY: y } = event
    dispatch({
      type, payload: { value }, meta: { x, y }
    })
  }

  return (
    <>
      <p>Count: {state.count}</p>
      <button onClick={(e) => handleClick('INC', 1, e)}>+1</button>
      <button onClick={(e) => handleClick('DEC', 1, e)}>-1</button>
      <button onClick={(e) => handleClick('INC', 2, e)}>+2</button>
      <button onClick={(e) => handleClick('DEC', 2, e)}>-2</button>
    </>
  )
}

export default App
```


