# Event Handlers

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
```

### App.jsx
```js
import './App.css'

function App() {

  function handleClick() {
    console.log('Event 1')
  }

  return (
    <>
      <button onClick={handleClick}>
        Button 1
      </button>
      <button onClick={() => {console.log('Event 2')}}>
        Button 2
      </button>
    </>
  )
}

export default App
```

<hr/>

### App.jsx
```js
import './App.css'
import Button from './Button'

function App() {

  return (
    <>
      <Button name={'Home'} />
      <Button name={'Store'} />
      <Button name={'Contact'} />
    </>
  )
}

export default App
```

### Button.jsx
```js
const Button = ({name}) => (
  <button 
    onClick={
      () => console.log(name)
    }
  >
    {name}
  </button>
)

export default Button
```

<hr/>


### Button.jsx
```js
const handleEvent = (name, which) => {
  console.log(name, which)
}

const Button = ({name}) => (
  <button 
    onMouseEnter={
      () => handleEvent(name, 'MouseEnter')
    }
    onMouseLeave={
      () => handleEvent(name, 'MouseLeave')
    }
    onDoubleClick={
      () => handleEvent(name, 'DoubleClick')
    }
    onContextMenu={
      () => handleEvent(name, 'onContextMenu')
    }
  >
    {name}
  </button>
)

export default Button
```

### Button.jsx
```js
const handleEvent = (name, e) => {
  console.log(name, e)
  console.log(name, e.clientX, e.clientY)
  console.log(name, e.shiftKey)
}

const Button = ({name}) => (
  <button 
    onClick={
      (e) => handleEvent(name, e)
    }
  >
    {name}
  </button>
)

export default Button
```

<hr/>

### App.jsx
```js
import './App.css'

function App() {

  return (
    <>
      <input
        onFocus={() => console.log('Focus')}
        onBlur={() => console.log('Blur')}
        onChange={(e) => console.log(e.target.value)}
        onKeyDown={(e) => {
          console.log(e.key, 'DOWN')
          if (e.key === 'Enter' && e.shiftKey) {
            console.log('Shift + Enter DOWN');
          }
        }}
        onKeyUp={(e) => {console.log(e.key, 'UP')}}
      />
    </>
  )
}

export default App
```
