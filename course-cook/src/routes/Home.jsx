import React, {useState} from "react";
import { Pane, Text } from 'evergreen-ui'

import Semesters from "../components/Semesters";

function Home() {
  const [semesterId, setSemesterId] = useState("");

	return (
    <Pane
      margin="1rem"
      padding="1rem"
      display="flex"
      border="default"
      flexDirection="column"
    >
      <Text>Select Semester</Text>
      <Semesters
        semesterId={semesterId}
        setSemesterId={setSemesterId}
      />
    </Pane>
	);
}

export default Home;
