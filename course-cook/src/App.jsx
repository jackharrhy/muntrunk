import React from 'react'
import { createClient, Provider } from 'urql';

import Routes from './Routes';

const client = createClient({ url: '/v1/graphql/' });

function App() {
	return (
    <Provider value={client}>
      <Routes />
    </Provider>
	);
}

export default App;
