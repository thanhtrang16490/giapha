import FamilyApp from '@/components/family-app';
import people from '@/data_json/people.json';
import records from '@/data_json/records.json';
export default function Page(){return <FamilyApp people={people} records={records}/>}
