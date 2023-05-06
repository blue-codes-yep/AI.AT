import React from 'react';
import { Carousel } from 'react-responsive-carousel';
import 'react-responsive-carousel/lib/styles/carousel.min.css';
import { Typography, Box } from '@mui/material';

const ImageResults = ({ imageResults }) => {
    return (
        <Box my={4}>
            <Typography variant="h4" align="center" gutterBottom>
                Image Results
            </Typography>
            <Carousel showThumbs={false} showStatus={false}>
                {imageResults.map((imageUrl, index) => (
                    <div key={index}>
                        <a href={imageUrl} target="_blank" rel="noopener noreferrer">
                            <img src={imageUrl} alt={`Image ${index + 1}`} />
                        </a>
                    </div>
                ))}
            </Carousel>
        </Box>
    );
};

export default ImageResults;
