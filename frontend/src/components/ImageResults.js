import React from 'react';
import { Carousel } from 'react-responsive-carousel';
import 'react-responsive-carousel/lib/styles/carousel.min.css';
import { IconButton } from '@mui/material';
import ArrowBackIosIcon from '@mui/icons-material/ArrowBackIos';
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';

const ImageResults = ({ imageResults }) => {
    const arrowStyles = {
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
        borderRadius: '50%',
        padding: '5px',
        zIndex: 2,
    };

    const CustomArrowPrev = (onClickHandler, hasPrev, label) => (
        <IconButton
            onClick={onClickHandler}
            disabled={!hasPrev}
            title={label}
            style={{ ...arrowStyles, position: 'absolute', left: 15, top: 'calc(50% - 20px)' }}
        >
            <ArrowBackIosIcon style={{ color: 'white' }} />
        </IconButton>
    );

    const CustomArrowNext = (onClickHandler, hasNext, label) => (
        <IconButton
            onClick={onClickHandler}
            disabled={!hasNext}
            title={label}
            style={{ ...arrowStyles, position: 'absolute', right: 15, top: 'calc(50% - 20px)' }}
        >
            <ArrowForwardIosIcon style={{ color: 'white' }} />
        </IconButton>
    );

    return (
        <div className="image-results">
            <h2>Image Results</h2>
            <Carousel
                showArrows
                showThumbs={false}
                renderArrowPrev={CustomArrowPrev}
                renderArrowNext={CustomArrowNext}
            >
                {imageResults.map((imageUrl, index) => (
                    <div key={index}>
                        <img
                            src={imageUrl}
                            alt={`Image ${index + 1}`}
                            style={{
                                maxWidth: '892px',
                                maxHeight: '572px',
                                objectFit: 'contain',
                                width: '100%',
                                height: '100%',
                            }}
                        />
                    </div>
                ))}
            </Carousel>
        </div>
    );
};

export default ImageResults;
