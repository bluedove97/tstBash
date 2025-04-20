# Component Props

### Card.module.css
```css
.card {
  width: 224px;
  margin: 12px auto;
  padding: 24px;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card h2 {
  margin: 0 0 8px;
  font-size: 1.33rem;
  color: #333;
}

.card p {
  margin: 2px 0;
}

.card p:last-child {
  font-size: 0.92rem;
  color: #888;
}
```

### InfoCard.jsx
```js
import styles from './Card.module.css'

const InfoCard = (props) => (
  <div className={styles.card}>
    <h2>{props.title}</h2>
    <p>{props.content}</p>
    <p>Author: {props.author}</p>
  </div>
)

export default InfoCard
```

### App.jsx
```js
import './App.css'

import InfoCard from './InfoCard'

function App() {

  return (
    <>
      <InfoCard 
        title="Props in React"
        content="Props pass data from one component to another."
        author="Alice"
      />
      <InfoCard 
        title="React Composition"
        content="Composition makes your components more reusable"
        author="Charlie"
      />
    </>
  )
}

export default App
```
<hr/>

### InfoCard.jsx
```js
import styles from './Card.module.css'

const InfoCard = ({ title, content, author }) => (
  <div className={styles.card}>
    <h2>{title}</h2>
    <p>{content}</p>
    <p>Author: {author}</p>
  </div>
)

export default InfoCard
```

### InfoCard.jsx
```js
import styles from './Card.module.css'

const InfoCard = ({ 
  title="(No Title)",
  content,
  author="Anonymous" 
}) => (
  <div className={styles.card}>
    <h2>{title}</h2>
    <p>{content}</p>
    <p>Author: {author}</p>
  </div>
)

export default InfoCard
```

### App.jsx
```js
import './App.css'

import InfoCard from './InfoCard'

function App() {

  return (
    <>
      <InfoCard 
        title="Props in React"
        content="Props pass data from one component to another."
        author="Alice"
      />
      <InfoCard 
        title="React Composition"
        content="Composition makes your components more reusable"
      />
    </>
  )
}

export default App
```

### App.jsx
```js
import './App.css'

import InfoCard from './InfoCard'

const cardData1 = {
  title: "Props in React",
  content: "Props pass data from one component to another.",
  author: "Alice"
};
const cardData2 = {
  title: "React Composition",
  content: "Composition makes your components more reusable"
};

function App() {

  return (
    <>
      <InfoCard {...cardData1} />
      <InfoCard {...cardData2} />
    </>
  )
}

export default App
```


### App.jsx
```js
import './App.css'

import InfoCard from './InfoCard'

const cards = [
  {
    idx: 1,
    title: "Props in React",
    content: "Props pass data from one component to another.",
    author: "Alice"
  }, {
    idx: 2,
    title: "React Composition",
    content: "Composition makes your components more reusable"
  }
]

function App() {

  return (
    <>
      {cards.map(cardData => (
        <InfoCard key={cardData.idx} {...cardData} />
      ))}
    </>
  )
}

export default App
```

<hr/>

### ProductCard.jsx
```js
import styles from './Card.module.css'

const ProductCard = ({ 
  name, price, formatPrice 
}) => {
  const displayedPrice
   = formatPrice(price)

  return (
    <div className={styles.card}>
      <h2>{name}</h2>
      <p>Price: {displayedPrice}</p>
    </div>
  );
}

export default ProductCard
```

### App.jsx
```js
import './App.css'

import ProductCard from './ProductCard'

const App = () => {
  const product = { 
    name: "Laptop", 
    price: 123.4567 
  };

  return (
    <ProductCard 
    {...product} 
    formatPrice={(p) => `$${p.toFixed(2)}`}
    />
  );
}

export default App
```
