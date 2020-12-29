interface VotationTitle {
  language_code: string
  title: string
}

export interface SimpleVotation {
  id: number
  titles: VotationTitle[]
  is_finished: boolean
  needs_staende: boolean
  is_accepted: boolean
  yes_counted: number
  no_counted: number
  yes_predicted: number
  no_predicted: number
  counted_communes: number
  predicted_communes: number
  date_id: number
}

export interface VotationDate {
  id: number
  start_date: Date
  votations: SimpleVotation[]
  is_finished: boolean
}

export interface Result {
  yes_total: number
  no_total: number
  is_final: boolean
  geo_id: number
  name: string
}

export interface CommuneResult extends Result {
  participation: number
  canton: number
}

export interface CantonResult extends Result {
  yes_predicted: number
  no_predicted: number
}

export interface Votation extends SimpleVotation {
  communes: CommuneResult[]
  cantons: CantonResult[]
  timestamp: Date
}

export function getTitle(
  votation: SimpleVotation,
  language_code: string
): string {
  const title = votation.titles.find(
    (title) => title.language_code == language_code
  )

  if (title) {
    return title.title
  }

  return ''
}

interface VotationDataPoint {
  name: Date
  value: number
}

export interface VotationDataSeries {
  name: string
  series: VotationDataPoint[]
}

export interface RelatedResult {
  y: number
  n: number
  title: string
}
