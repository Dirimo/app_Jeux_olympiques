export default function OlympicRings({className = "w-16 h-8" }) {
    return (
        <svg
            className={className}
            viewBox="0 0 1020 495"
            xmlns="http://www.w3.org/2000/svg"
        >
            {/* Blue */}
            <circle
                cx="120" cy="120" r="90" fill="none" stroke="#0085C7" strokeWidth="18"
            />
            {/* Jaune */}
            <circle
                cx="300" cy="120" r="90" fill="none" stroke="#FCB131" strokeWidth="18"
            />
            {/* Noir */}
            <circle
                cx="540" cy="120" r="90" fill="none" stroke="#000000" strokeWidth="18"
            />  
            {/* Vert */}
            <circle
                cx="225" cy="240" r="90" fill="none" stroke="#009F3D" strokeWidth="18"
            />
            {/* Rouge */}
            <circle
                cx="435" cy="240" r="90" fill="none" stroke="#EE334E" strokeWidth="18"
            />
        </svg>
    );
}