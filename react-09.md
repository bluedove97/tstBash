# Optimization

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

### Before
<code>App.jsx</code>
```js
import './App.css'
import { useState } from 'react'

function App() {
  const [count1, setCount1] = useState(0)
  const [count2, setCount2] = useState(0)

  const heavyCalculation = (num) => {
    console.log('Calculating...')
    let result = 0
    for (let i = 0; i < 1000000000; i++) {
      result += num
    }
    return result
  }

  return (
    <>
      <p>Counter 1: {count1}</p>
      <button onClick={
        () => setCount1(count1 + 1)
      }>+</button>
      <button onClick={
        () => setCount1(count1 - 1)
      }>-</button>
      <p>Counter 2: {
        heavyCalculation(count2)
      }</p>
      <button onClick={
        () => setCount2(count2 + 1)
      }>+</button>
      <button onClick={
        () => setCount2(count2 - 1)
      }>-</button>
    </>
  )
}

export default App
```

### After
<code>App.jsx</code>
```js
import './App.css'
import { useState, useMemo } from 'react'

function App() {
  const [count1, setCount1] = useState(0)
  const [count2, setCount2] = useState(0)

  const heavyCalculation = (num) => {
    console.log('Calculating...')
    let result = 0
    for (let i = 0; i < 1000000000; i++) {
      result += num
    }
    return result
  }

  const calculatedValue = useMemo(
    () => heavyCalculation(count2), [count2])

  return (
    <>
      <p>Counter 1: {count1}</p>
      <button onClick={
        () => setCount1(count1 + 1)
      }>+</button>
      <button onClick={
        () => setCount1(count1 - 1)
      }>-</button>
      <p>Counter 2: {calculatedValue}</p>
      <button onClick={
        () => setCount2(count2 + 1)
      }>+</button>
      <button onClick={
        () => setCount2(count2 - 1)
      }>-</button>
    </>
  )
}

export default App
```

<hr/>

<code>App.jsx</code>
```js
import './App.css'
import { useState } from 'react'
import Child from './Child'

function App() {
  const [count, setCount] = useState(0)
  const [active, setActive] = useState(true)

  return (
    <>
      <h2>Parent</h2>
      <button onClick={
        () => setCount(count + 1)
      }>Increase</button>
      <button onClick={
        () => setActive(a => !a)
      }>Change Name</button>
      <p>Count: {count}</p>
      <Child active={active} />
    </>
  )
}

export default App
```

### Before
<code>Child.jsx</code>
```js
import React from 'react'

function Child({ active }) {
  console.log(
    'Child rendered'
  )
  return (
    <p>
      Child: {
        active ? 'Active' : 'Not active'
      }
    </p>
  )
}

export default Child
```

### After
<code>Child.jsx</code>
```js
import React from 'react'

function Child({ active }) {
  console.log(
    'Child rendered'
  )
  return (
    <p>
      Child: {
        active ? 'Active' : 'Not active'
      }
    </p>
  )
}

export default React.memo(Child)
```

<hr/>

<code>Child.jsx</code>
```js
import React from 'react'

function Child({ active, onClick }) {
  console.log(
    'Child rendered'
  )

  return (
    <div>
      <p>Child: {
        active ? 'Active' : 'Not active'
      }</p>
      <button onClick={onClick}>
        Increase
      </button>
    </div>
  )
}

export default React.memo(Child)
```

### Before

<code>App.jsx</code>
```js
import './App.css'
import { useState } from 'react'
import Child from './Child'

function App() {
  const [count, setCount] = useState(0)
  const [active, setActive] = useState(true)

  return (
    <>
      <h2>Parent</h2>
      <button onClick={
        () => setActive(a => !a)
      }>Toggle Active</button>
      <p>Count: {count}</p>
      <Child
        active={active} 
        onClick={() => setCount(c => c + 1)} />
    </>
  )
}

export default App
```

### After

<code>App.jsx</code>
```js
import './App.css'
import { useState, useCallback } from 'react'
import Child from './Child'

function App() {
  const [count, setCount] = useState(0)
  const [active, setActive] = useState(true)

  const handleClick = useCallback(
    () => { setCount(c => c + 1) }, [])

  return (
    <>
      <h2>Parent</h2>
      <button onClick={() => setActive(a => !a)}>
        Toggle Active
      </button>
      <p>Count: {count}</p>
      <Child active={active} 
        onClick={handleClick} />
    </>
  )
}
export default App
```
