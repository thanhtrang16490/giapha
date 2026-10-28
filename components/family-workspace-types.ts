import type {Person} from './family-types';
export type Entry={id:string;title:string;content?:string;createdAt:string;updatedAt:string;archived?:boolean;[key:string]:string|number|boolean|undefined};
export type FamilySettings={name:string;location:string;motto:string;description:string;theme:string};
export type WorkspaceState={version:number;revision:number;settings:FamilySettings;collections:Record<string,Entry[]>;audit:{id:string;at:string;action:string;target:string;label:string}[];reviews:Record<string,{status:string;at:string}>};
export type Contribution={id:string;name:string;content:string;createdAt:string;status:string};
export type WorkspaceData={people:Person[];state:WorkspaceState;archivedPeople:Person[];contributions:Contribution[]};
export type Mutate=(action:string,data?:Record<string,unknown>,id?:string,collection?:string)=>Promise<void>;
