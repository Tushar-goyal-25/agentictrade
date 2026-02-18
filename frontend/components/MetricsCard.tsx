interface MetricsCardProps {
  label: string;
  value: string;
  negative?: boolean;
}

export default function MetricsCard({ label, value, negative = false }: MetricsCardProps) {
  return (
    <div className="bg-gray-50 rounded-lg p-3">
      <p className="text-xs text-gray-600 mb-1">{label}</p>
      <p className={`text-lg font-bold ${negative ? 'text-red-600' : 'text-gray-900'}`}>
        {value}
      </p>
    </div>
  );
}
