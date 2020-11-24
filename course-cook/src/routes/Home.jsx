import React, { useState } from "react";

import Semesters from "../components/Semesters";
import Subjects from "../components/Subjects";
import Courses from "../components/Courses";

function Home() {
  const [semesterId, setSemesterId] = useState("");
  const [subjectId, setSubjectId] = useState("");

  return (
    <div>
      <div id="filters">
        <Semesters semesterId={semesterId} setSemesterId={setSemesterId} />
        <Subjects subjectId={subjectId} setSubjectId={setSubjectId} />
      </div>
      <div id="courses">
        {(semesterId !== "" && subjectId !== "") ? (
          <Courses semesterId={semesterId} subjectId={subjectId} />
        ) : (
          <p id="no-filters">^ Select some filters above ^</p>
        )}
      </div>
    </div>
  );
}

export default Home;
