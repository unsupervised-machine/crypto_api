import { useState, useEffect } from 'react';
import {
  Table,
  ScrollArea,
  UnstyledButton,
  Group,
  Text,
  Center,
  TextInput,
  rem,
} from '@mantine/core';
import { IconSelector, IconChevronDown, IconChevronUp, IconSearch } from '@tabler/icons-react';
import classes from './TableSort.module.css';

// Import your cryptocurrency data
import cryptoData from '../../MOCK_DATA/table_data.json';

interface RowData {
  image: string;
  id: string;
  symbol: string;
  name: string;
  current_price: number;
}

interface ThProps {
  children: React.ReactNode;
  reversed: boolean;
  sorted: boolean;
  onSort(): void;
}

function Th({ children, reversed, sorted, onSort }: ThProps) {
  const Icon = sorted ? (reversed ? IconChevronUp : IconChevronDown) : IconSelector;
  return (
    <Table.Th className={classes.th}>
      <UnstyledButton onClick={onSort} className={classes.control}>
        <Group justify="space-between">
          <Text fw={500} fz="sm">
            {children}
          </Text>
          <Center className={classes.icon}>
            <Icon style={{ width: rem(16), height: rem(16) }} stroke={1.5} />
          </Center>
        </Group>
      </UnstyledButton>
    </Table.Th>
  );
}

function filterData(data: RowData[], search: string) {
  const query = search.toLowerCase().trim();
  return data.filter((item) =>
    Object.keys(item).some((key) => item[key as keyof RowData].toString().toLowerCase().includes(query))
  );
}

function sortData(
  data: RowData[],
  payload: { sortBy: keyof RowData | null; reversed: boolean; search: string }
) {
  const { sortBy } = payload;

  if (!sortBy) {
    return filterData(data, payload.search);
  }

  return filterData(
    [...data].sort((a, b) => {
      if (payload.reversed) {
        return b[sortBy].toString().localeCompare(a[sortBy].toString());
      }

      return a[sortBy].toString().localeCompare(b[sortBy].toString());
    }),
    payload.search
  );
}

export function Table_w_images() {
  const [data, setData] = useState<RowData[]>([]);
  const [search, setSearch] = useState('');
  const [sortedData, setSortedData] = useState<RowData[]>([]);
  const [sortBy, setSortBy] = useState<keyof RowData | null>(null);
  const [reverseSortDirection, setReverseSortDirection] = useState(false);

  useEffect(() => {
  // Map full data to only include necessary fields
  const mappedData: RowData[] = cryptoData.map((item: FullRowData) => ({
    id: item.id,
    symbol: item.symbol,
    name: item.name,
    current_price: item.current_price,
    image: item.image,
  }));

  setData(mappedData);
  setSortedData(mappedData); // Initially set sorted data same as original data
}, []);

  const headers = [
    { key: 'name', label: 'Coin' },
    // { key: 'symbol', label: 'Symbol' },
    // { key: 'name', label: 'Coin' },
    { key: 'current_price', label: '$USD' },
    // { key: 'image', label: 'Image' }, // Assuming an image column
  ];

  const setSorting = (field: keyof RowData) => {
    const reversed = field === sortBy ? !reverseSortDirection : false;
    setReverseSortDirection(reversed);
    setSortBy(field);
    setSortedData(sortData(data, { sortBy: field, reversed, search }));
  };

  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { value } = event.currentTarget;
    setSearch(value);
    setSortedData(sortData(data, { sortBy, reversed: reverseSortDirection, search: value }));
  };

  const rows = sortedData.map((row) => (
    <Table.Tr key={row.name}>
      <Table.Td>
        {row.image && <img src={row.image} alt={`${row.name} Image`} style={{ width: '50px', height: 'auto' }} />}
        <div className={classes.text}>
          <div>{`${row.name} - ${row.symbol}`}</div>
        </div>
      </Table.Td>
      {/*<Table.Td>{`${row.name} - ${row.symbol}`}</Table.Td>*/}
      {/*<Table.Td>{row.symbol}</Table.Td>*/}
      <Table.Td>${row.current_price}</Table.Td>
    </Table.Tr>
  ));


  const colSpanValue = headers.length;

  return (
    <ScrollArea>
      <TextInput
        placeholder="Search by any field"
        mb="md"
        leftSection={<IconSearch style={{ width: rem(16), height: rem(16) }} stroke={1.5} />}
        value={search}
        onChange={handleSearchChange}
      />
      <Table striped highlightOnHover withTableBorder withColumnBorders horizontalSpacing="md" verticalSpacing="xs" miw={700} layout="fixed">
        <Table.Tbody>
          <Table.Tr>
            {headers.map((header) => (
              <Th
                key={header.key}
                sorted={sortBy === header.key}
                reversed={reverseSortDirection}
                onSort={() => setSorting(header.key as keyof RowData)}
              >
                {header.label}
              </Th>
            ))}
          </Table.Tr>
        </Table.Tbody>
        <Table.Tbody>
          {rows.length > 0 ? (
            rows
          ) : (
            <Table.Tr>
              <Table.Td colSpan={colSpanValue}>
                <Text fw={500} ta="center">
                  Nothing found
                </Text>
              </Table.Td>
            </Table.Tr>
          )}
        </Table.Tbody>
      </Table>
    </ScrollArea>
  );
}
