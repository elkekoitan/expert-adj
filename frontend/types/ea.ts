export type Platform = 'MT4' | 'MT5'
export type ParameterType = 'int' | 'double' | 'string' | 'bool' | 'enum'

export interface ExpertAdvisor {
  id: string
  name: string
  description?: string
  platform: Platform
  tags?: string[]
  is_active: boolean
  owner_id: string
  organization_id?: string
  created_at: string
  updated_at: string
}

export interface EAVersion {
  id: string
  ea_id: string
  version: string
  build_hash: string
  compiled_file_path: string
  source_file_path?: string
  source_present: boolean
  requires_sdk: boolean
  compiled_at?: string
  created_at: string
}

export interface EAParameter {
  id: string
  ea_version_id: string
  name: string
  parameter_type: ParameterType
  default_value: string
  min_value?: string
  max_value?: string
  step_value?: string
  enum_values?: string[]
  description?: string
  is_optimizable: boolean
  group_name?: string
  sort_order: number
}

export interface ParameterGroup {
  name: string
  parameters: EAParameter[]
}

export interface EAParameterPreset {
  id: string
  ea_version_id: string
  name: string
  description?: string
  parameter_values: Record<string, any>
  tags?: string[]
  performance_metrics?: Record<string, any>
  is_template: boolean
  is_public: boolean
  is_favorite: boolean
  owner_id: string
  created_at: string
  updated_at: string
}

export interface EAUploadResponse {
  ea: ExpertAdvisor
  version: EAVersion
  parameters: {
    extracted: number
    summary: {
      optimizable_count: number
      group_count: number
      groups: string[]
    }
    details: EAParameter[]
  }
}
