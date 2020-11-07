import React from 'react';
import {useQuery} from 'graphql-hooks'
import {Box, CheckBox} from 'grommet';

export default function MultiSelect({
  query,
  converter,
  findKey,
  findLabel,
  checked,
  setChecked,
}) {
  const {loading, error, data} = useQuery(query);

  if (loading) return <p>loading</p>
  if (error) return <p>Someting went wrong!</p>

  const options = converter(data);

  console.log(checked);

  const onCheckAll = (event) => {
    if (event.target.checked) {
      console.log('check all');
      // setChecked(checkboxes);
    } else {
      setChecked([]);
    }
  };

  const onCheck = (event, value) => {
    if (event.target.checked) {
      setChecked([...checked, value]);
    } else {
      setChecked(checked.filter((item) => item !== value));
    }
  };

  return (
    <Box
      direction="column"
      gap="medium"
      overflowY="scroll"
      height="100%"
    >
      <CheckBox
        checked={checked.length === options.length}
        indeterminate={checked.length > 0 && checked.length < options.length}
        label="All"
        onChange={onCheckAll}
      />
      {options.map((item) => (
        <CheckBox
          key={findKey(item)}
          checked={checked.includes(item.id)}
          label={findLabel(item)}
          onChange={(e) => onCheck(e, item.id)}
        />
      ))}
    </Box>
  );
}
