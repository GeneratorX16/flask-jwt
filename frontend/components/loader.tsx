import { TailSpin } from 'react-loader-spinner';

const LoadingSpinner = ({dim, color, radius, visible}: {dim?: string, color?: string, radius?: string, visible?: boolean}) => {

    return (
        <TailSpin
            visible={visible ?? true}
            height={dim ?? "14"}
            width={dim ?? "14"}
            color={color ?? "black"}
            ariaLabel="tail-spin-loading"
            radius={radius ?? "1"}
            wrapperStyle={{}}
            wrapperClass=""
        />
    );
};

export default LoadingSpinner;