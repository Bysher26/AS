import math

class DosageCalculator:
    def __init__(self, weight_kg, age_years):
        self.weight = weight_kg
        self.age = age_years
    
    def get_airway_defib_medications(self):
        """Calculate airway and defibrillation medication dosages"""
        medications = [
            {
                'name': 'ETT Size',
                'dosage': f'{round((self.age + 16) / 4 * 2) / 2:.1f}mm' if self.age < 8 else '7.0-8.0mm',
                'route': 'Endotracheal tube'
            },
            {
                'name': 'ETT Depth',
                'dosage': f'{(self.age / 2) + 12:.0f}cm' if self.age < 10 else '21-23cm',
                'route': 'At the lips'
            },
            {
                'name': 'Laryngoscopy Blade',
                'dosage': '1' if self.age < 2 else ('2' if self.age < 10 else '3'),
                'route': 'Miller (straight) or Macintosh (curved)'
            },
            {
                'name': 'LMA Size',
                'dosage': self._get_lma_size(),
                'route': 'Laryngeal mask airway'
            },
            {
                'name': 'Defibrillation (2-4 J/kg)',
                'dosage': f'{self.weight * 2:.0f} - {self.weight * 4:.0f} J',
                'route': 'External paddles/pads'
            },
            {
                'name': 'Sync. Cardioversion (0.5-1-2 J/kg)',
                'dosage': f'{self.weight * 0.5:.1f} - {self.weight * 1:.0f} - {self.weight * 2:.0f} J',
                'route': 'Synchronized'
            }
        ]
        return medications
    
    def get_intubation_medications(self):
        """Calculate intubation medication dosages"""
        medications = [
            {
                'name': 'Ketamine (1mg/kg)',
                'dosage': f'{self.weight * 1:.1f} mg',
                'route': 'IV/IO, Max dose: 100mg'
            },
            {
                'name': 'Midazolam (0.1mg/kg)',
                'dosage': f'{self.weight * 0.1:.1f} mg',
                'route': 'IV/IO, Max dose: 5mg'
            },
            {
                'name': 'Fentanyl (1-3mcg/kg)',
                'dosage': f'{self.weight * 1:.0f} - {self.weight * 3:.0f} mcg',
                'route': 'IV/IO, Max dose: 100mcg'
            },
            {
                'name': 'Morphine (0.1mg/kg)',
                'dosage': f'{self.weight * 0.1:.1f} mg',
                'route': 'IV/IO, Max dose: 10mg'
            },
            {
                'name': 'Thiopental (3-5mg/kg)',
                'dosage': f'{self.weight * 3:.0f} - {self.weight * 5:.0f} mg',
                'route': 'IV/IO, Max dose: 250mg'
            },
            {
                'name': 'Propofol (1-3mg/kg)',
                'dosage': f'{self.weight * 1:.0f} - {self.weight * 3:.0f} mg',
                'route': 'IV/IO, Max dose: 300mg'
            },
            {
                'name': 'Rocuronium (1mg/kg)',
                'dosage': f'{self.weight * 1:.0f} mg',
                'route': 'IV/IO, Max dose: 100mg'
            },
            {
                'name': 'Suxamethonium (1.5mg/kg)',
                'dosage': f'{self.weight * 1.5:.0f} mg',
                'route': 'IV/IO, Max dose: 150mg'
            },
            {
                'name': 'Neostigmine (0.05mg/kg)',
                'dosage': f'{self.weight * 0.05:.2f} mg',
                'route': 'IV/IO, Max dose: 2.5mg'
            },
            {
                'name': 'Sugammadex (4mg/kg)',
                'dosage': f'{self.weight * 4:.0f} mg',
                'route': 'IV/IO, Max dose: 400mg'
            },
            {
                'name': 'Atropine (0.02mg/kg)',
                'dosage': f'{self.weight * 0.02:.2f} mg',
                'route': 'IV/IO, Min: 0.1mg, Max: 0.6mg'
            }
        ]
        return medications
    
    def get_emergency_medications(self):
        """Calculate emergency medication dosages"""
        medications = [
            {
                'name': 'Adrenaline 1:10,000 (0.01mg/kg)',
                'dosage': f'{self.weight * 0.01:.2f} mg = {self.weight * 0.1:.1f} ml',
                'route': 'IV/IO, Max dose: 1mg'
            },
            {
                'name': 'Adrenaline 1:1,000 ET (0.1mg/kg)',
                'dosage': f'{self.weight * 0.1:.1f} mg = {self.weight * 0.1:.1f} ml',
                'route': 'Endotracheal, Max dose: 10mg'
            },
            {
                'name': 'Adrenaline 1:1,000 IM (0.01mg/kg)',
                'dosage': f'{self.weight * 0.01:.2f} mg = {self.weight * 0.01:.2f} ml',
                'route': 'Intramuscular, Max dose: 0.5mg'
            },
            {
                'name': 'Atropine (0.02mg/kg)',
                'dosage': f'{self.weight * 0.02:.2f} mg',
                'route': 'IV/IO, Min: 0.1mg, Max: 3mg'
            },
            {
                'name': 'Amiodarone (5mg/kg)',
                'dosage': f'{self.weight * 5:.0f} mg',
                'route': 'IV/IO, Max dose: 300mg'
            },
            {
                'name': 'ATP (0.1mg/kg)',
                'dosage': f'{self.weight * 0.1:.1f} mg',
                'route': 'IV/IO, Max dose: 6mg'
            },
            {
                'name': 'Calcium gluconate (0.1ml/kg 10%)',
                'dosage': f'{self.weight * 0.1:.1f} ml',
                'route': 'IV/IO, Max dose: 20ml'
            },
            {
                'name': 'Dextrose D10 (2.5ml/kg)',
                'dosage': f'{self.weight * 2.5:.1f} ml',
                'route': 'IV/IO, Max dose: 250ml'
            },
            {
                'name': 'Dextrose D50 (0.5ml/kg)',
                'dosage': f'{self.weight * 0.5:.1f} ml',
                'route': 'IV/IO, Max dose: 50ml'
            },
            {
                'name': 'Flumazenil (0.01mg/kg)',
                'dosage': f'{self.weight * 0.01:.2f} mg',
                'route': 'IV/IO, Max dose: 2mg'
            },
            {
                'name': 'Lignocaine 2% (1mg/kg)',
                'dosage': f'{self.weight * 1:.0f} mg',
                'route': 'IV/IO, Max dose: 100mg'
            },
            {
                'name': 'Lorazepam (0.1mg/kg)',
                'dosage': f'{self.weight * 0.1:.1f} mg',
                'route': 'IV/IO, Max dose: 4mg'
            },
            {
                'name': 'Midazolam (0.1mg/kg)',
                'dosage': f'{self.weight * 0.1:.1f} mg',
                'route': 'IV/IO, Max dose: 10mg'
            },
            {
                'name': 'MgSO4 50% (50mg/kg)',
                'dosage': f'{self.weight * 50:.0f} mg',
                'route': 'IV/IO, Max dose: 2g'
            },
            {
                'name': 'Naloxone (0.1mg/kg)',
                'dosage': f'{self.weight * 0.1:.1f} mg',
                'route': 'IV/IO/IM, Max dose: 2mg'
            },
            {
                'name': 'NaHCO3 8.4% (1ml/kg)',
                'dosage': f'{self.weight * 1:.0f} ml',
                'route': 'IV/IO, Max dose: 50ml'
            },
            {
                'name': 'Procainamide (15mg/kg)',
                'dosage': f'{self.weight * 15:.0f} mg',
                'route': 'IV/IO, Max dose: 1000mg'
            }
        ]
        return medications
    
    def get_inotropes(self):
        """Calculate inotrope dosages and infusion rates"""
        medications = [
            {
                'name': 'Dopamine',
                'dosage': f'{self.weight:.1f} kg',
                'route': '5-20 mcg/kg/min infusion'
            },
            {
                'name': 'Dobutamine',
                'dosage': f'{self.weight:.1f} kg',
                'route': '5-20 mcg/kg/min infusion'
            },
            {
                'name': 'Adrenaline',
                'dosage': f'{self.weight:.1f} kg',
                'route': '0.01-0.4 mcg/kg/min infusion'
            },
            {
                'name': 'Adrenaline (high conc.)',
                'dosage': f'{self.weight:.1f} kg',
                'route': '0.4-4 mcg/kg/min infusion'
            },
            {
                'name': 'Noradrenaline',
                'dosage': f'{self.weight:.1f} kg',
                'route': '0.01-0.4 mcg/kg/min infusion'
            },
            {
                'name': 'Noradrenaline (high conc.)',
                'dosage': f'{self.weight:.1f} kg',
                'route': '0.4-4 mcg/kg/min infusion'
            },
            {
                'name': 'Milrinone',
                'dosage': f'{self.weight:.1f} kg',
                'route': '0.25-1 mcg/kg/min infusion'
            },
            {
                'name': 'Vasopressin',
                'dosage': f'{self.weight:.1f} kg',
                'route': '0.01-0.12 units/kg/h infusion'
            }
        ]
        return medications
    
    def get_sedation_paralysis(self):
        """Calculate sedation and paralysis medication dosages"""
        medications = [
            {
                'name': 'Fentanyl',
                'dosage': f'{self.weight:.1f} kg',
                'route': '1-4 mcg/kg/h infusion'
            },
            {
                'name': 'Morphine',
                'dosage': f'{self.weight:.1f} kg',
                'route': '10-40 mcg/kg/h infusion'
            },
            {
                'name': 'Midazolam',
                'dosage': f'{self.weight:.1f} kg',
                'route': '0.5-20 mcg/kg/h infusion'
            },
            {
                'name': 'Ketamine',
                'dosage': f'{self.weight:.1f} kg',
                'route': '1-10 mcg/kg/h infusion'
            },
            {
                'name': 'Dexmedetomidine',
                'dosage': f'{self.weight:.1f} kg',
                'route': '0.2-1.4 mcg/kg/h infusion'
            },
            {
                'name': 'Rocuronium',
                'dosage': f'{self.weight:.1f} kg',
                'route': '5-15 mcg/kg/min infusion'
            },
            {
                'name': 'Thiopentone',
                'dosage': f'{self.weight:.1f} kg',
                'route': '1-5 mg/kg/h infusion'
            }
        ]
        return medications
    
    def get_antihypertensives(self):
        """Calculate antihypertensive medication dosages"""
        medications = [
            {
                'name': 'Labetalol (undiluted)',
                'dosage': f'{self.weight:.1f} kg',
                'route': '0.25-3 mg/kg/h infusion'
            },
            {
                'name': 'Esmolol (undiluted)',
                'dosage': f'{self.weight:.1f} kg',
                'route': '25-300 mcg/kg/min infusion'
            },
            {
                'name': 'Nitroprusside',
                'dosage': f'{self.weight:.1f} kg',
                'route': '0.5-10 mcg/kg/min infusion'
            }
        ]
        return medications
    
    def get_antiarrhythmics(self):
        """Calculate antiarrhythmic medication dosages"""
        medications = [
            {
                'name': 'Amiodarone',
                'dosage': f'{self.weight:.1f} kg',
                'route': '5-15 mcg/kg/min infusion'
            },
            {
                'name': 'Lignocaine',
                'dosage': f'{self.weight:.1f} kg',
                'route': '15-50 mcg/kg/min infusion'
            },
            {
                'name': 'Procainamide',
                'dosage': f'{self.weight:.1f} kg',
                'route': '20-80 mcg/kg/min infusion'
            },
            {
                'name': 'Isoprenaline',
                'dosage': f'{self.weight:.1f} kg',
                'route': '0.05-1 mcg/kg/min infusion'
            }
        ]
        return medications
    
    def get_others(self):
        """Calculate other medication dosages"""
        medications = [
            {
                'name': 'Ventolin',
                'dosage': f'{self.weight:.1f} kg',
                'route': '1-5 mcg/kg/min infusion'
            },
            {
                'name': 'Aminophylline',
                'dosage': f'{self.weight:.1f} kg',
                'route': '0.5-1 mg/kg/h infusion'
            },
            {
                'name': 'Lasix',
                'dosage': f'{self.weight:.1f} kg',
                'route': '0.25-1 mg/kg/h infusion'
            },
            {
                'name': 'Actrapid',
                'dosage': f'{self.weight:.1f} kg',
                'route': '0.05-0.1 units/kg/h infusion'
            }
        ]
        return medications
    
    def _get_lma_size(self):
        """Determine LMA size based on weight"""
        if self.weight < 5:
            return "1"
        elif self.weight < 10:
            return "1.5"
        elif self.weight < 20:
            return "2"
        elif self.weight < 30:
            return "2.5"
        elif self.weight < 50:
            return "3"
        elif self.weight < 70:
            return "4"
        else:
            return "5"
    
    def _calculate_infusion_rate(self, weight, min_dose, max_dose, concentration=None):
        """Calculate infusion rate range for continuous infusions"""
        # Simplified calculation for display purposes
        # In practice, this would need concentration and preparation details
        min_rate = weight * min_dose * 0.06  # Approximate conversion
        max_rate = weight * max_dose * 0.06
        return f"{min_rate:.1f}-{max_rate:.1f}"
